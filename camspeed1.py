# %pip install -q -U gdown==5.2.0 supervision==0.24.0 ultralytics==8.3.12 lapx==0.5.11
import os
import subprocess
import warnings
from collections import defaultdict
from typing import Any
import supervision as sv

import matplotlib
matplotlib.use('TkAgg') # or 'TkAgg', 'QtAgg', 'Agg' etc.
import matplotlib.pyplot as plt

import gdown
import time
import numpy as np
import pandas as pd
import seaborn as sns

from IPython.display import Video
from IPython.display import Image
from numpy.typing import ArrayLike, NDArray
from scipy.signal import savgol_filter
from ultralytics import YOLO
import cv2 as cv
##################visulization###########################################
from utils.classes import get_cls_dict
from utils3.classes3 import get_cls_dict3
from utils.visualization import BBoxVisualization
from utils3.visualization3 import BBoxVisualization3
######################################
from pypylon import pylon



TICKSIZE = 12
FONT_COLOR = "#4A4B52"
GRADIENT_COLOR = "#BAB8B8"
BACKGROUND_COLOR = "#FFFCFA"
# TEXT = r"\textrm{{{}}}"

MATPLOTLIB_THEME = {
    "axes.labelcolor": FONT_COLOR,
    "axes.labelsize": TICKSIZE,
    "axes.facecolor": BACKGROUND_COLOR,
    "axes.titlesize": 16,
    "axes.grid": False,
    "axes.spines.bottom": False,
    "axes.spines.left": False,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "xtick.labelsize": TICKSIZE,
    "xtick.color": FONT_COLOR,
    "ytick.labelsize": TICKSIZE,
    "ytick.color": FONT_COLOR,
    "figure.facecolor": BACKGROUND_COLOR,
    "figure.edgecolor": BACKGROUND_COLOR,
    "figure.titlesize": 16,
    "figure.dpi": 72,  # Locally Seaborn uses 72, meanwhile Kaggle 96.
    "text.color": FONT_COLOR,
    "font.size": TICKSIZE,
    # "text.usetex": True,
    "font.family": "Serif",
}
plt.rcParams.update(MATPLOTLIB_THEME)

#ON_KAGGLE = os.getenv("KAGGLE_KERNEL_RUN_TYPE") is not None
#VIDEO_URL = "https://drive.google.com/uc?export=download&id=17BLLWPJP4hpzLw135SI3rQPaWtItM0lR"


#**************************basler*********************
# Get the transport layer factory
tl_factory = pylon.TlFactory.GetInstance()

# Get a list of all available devices
devices = tl_factory.EnumerateDevices()
# Create InstantCamera objects for the first two devices
camera1 = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
camera2 = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))

# Open the cameras
camera1.Open()
camera1.Width.Value = camera1.Width.Max
camera1.Height.Value = camera1.Height.Max
camera2.Open()
camera2.Width.Value = camera2.Width.Max
camera2.Height.Value = camera2.Height.Max

# Set pixel format (e.g., to RGB8 for color cameras)
camera1.PixelFormat.Value = "RGB8"
#camera2.PixelFormat.Value = "Mono8"

# Start grabbing images (continuous grabbing)
camera1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
camera2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
resulting_fps1 = camera1.ResultingFrameRate.GetValue()
print(f"Resulting Frame Rate: {resulting_fps1} FPS")
resulting_fps2 = camera2.ResultingFrameRate.GetValue()
print(f"Resulting Frame Rate: {resulting_fps2} FPS")
FPS = resulting_fps1
grabResult1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
grabResult2 = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

if grabResult1.GrabSucceeded():
    imgstart1 = grabResult1.Array
    imgstart2 = grabResult2.Array
    # Now 'image_data' is a NumPy array containing the image pixels
    # ... (further processing of image_data) ...
else:
    print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)


imS = cv.resize(imgstart1, (960, 540))          ## Resize image
#cv.imshow("output", imS)    #Show image
#cv.waitKey(0) 



#SOURCE_VIDEO = gdown.cached_download(VIDEO_URL, "m6-motorway-trim.mp4")

#Image(imgstart1, width=960, height=540)

def imshow(img, figsize: tuple[int, int] = (11, 7)) -> None:
    plt.figure(figsize=figsize, tight_layout=True)
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    

###################enhancement########################
def convertScale(img_plate, alpha, beta):
    """Add bias and gain to an image with saturation arithmetics. Unlike
    cv2.convertScaleAbs, it does not take an absolute value, which would lead to
    nonsensical results (e.g., a pixel at 44 with alpha = 3 and beta = -210
    becomes 78 with OpenCV, when in fact it should become 0).
    """

    new_img = img_plate * alpha + beta
    new_img[new_img < 0] = 0
    new_img[new_img > 255] = 255
    return new_img.astype(np.uint8)



def automatic_brightness_and_contrast(img_plate, clip_hist_percent=25):
    gray = cv.cvtColor(img_plate, cv.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / ((maximum_gray - minimum_gray)+2)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = convertScale(img_plate, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)    

####################platedetection#####################
def platedetection(crop_img , tensorrt_model_plate)-> NDArray:

    result_plates = tensorrt_model_plate(crop_img,conf=0.7, verbose=False)
    detection_plates = sv.Detections.from_ultralytics(result_plates[0])
    print('detection2', detection_plates)
    if detection_plates is None:
        print('print-image empty platedetection2', detection_plates) #file_name? speed? cv.imwrite(home/desktop/chackoprtator , crop_img)
    for result_plate in result_plates:
        xywh = result_plate.boxes.xywh  # center-x, center-y, width, height
        xywhn = result_plate.boxes.xywhn  # normalized
        xyxy = result_plate.boxes.xyxy  # top-left-x, top-left-y, bottom-right-x, bottom-right-y
        xyxyn = result_plate.boxes.xyxyn  # normalized
        #names = [result_plate.names[cls.item()] for cls in result.boxes.cls.int()]  # class name of each box
        confs = result_plate.boxes.conf  # confidence score of each box
        print('name-class', confs)
        print('name-class', xyxyn)
    print('no result', xywh)
    print('result_plates', result_plates)
    return result_plates
##############################


######################OCR_1###d######################
def  ocr_1(frame_ocr1, img_plate, obj_class_id ,obj_speed , obj_coordinate, trt_model_ocr1) -> None:
    cv.imshow('before _enhance_plate', img_plate)
    img_plate = cv.bilateralFilter(img_plate, 11, 17, 17) 
    img_plate, alpha, beta = automatic_brightness_and_contrast(img_plate) #enhance plate
    cv.imshow('enhance_plate', img_plate)

    result_ocr1s = trt_model_ocr1(img_plate, conf=0.7, verbose=False)
    detection_ocr_1s = sv.Detections.from_ultralytics(result_ocr1s[0])
    print('detection_ocr_1s' , detection_ocr_1s)
    print('no any result because the model is not true')

    boxs_ocr_1 = detection_ocr_1s.xyxy
    conf_ocr_1 = detection_ocr_1s.confidence
    class_id_ocr_1 = detection_ocr_1s.class_id
    print('class-name_ocr1', detection_ocr_1s.data)
    print('class_id_ocr_1', class_id_ocr_1)

    vis3.draw_bboxes3(frame_ocr1, img_plate, img_plate, boxs_ocr_1 , conf_ocr_1, class_id_ocr_1, obj_class_id, obj_speed, obj_coordinate)

    return
###############################
#################################ocr_2#################################
def  ocr_2(frame_ocr2, img_plate, obj_class_id ,obj_speed , obj_coordinate, trt_model_ocr2) -> None:
    cv.imshow('before _enhance_plate', img_plate)
    img_plate = cv.bilateralFilter(img_plate, 11, 17, 17) 
    img_plate, alpha, beta = automatic_brightness_and_contrast(img_plate) #enhance plate
    cv.imshow('enhance_plate', img_plate)

    result_ocr2s = trt_model_ocr2(img_plate, conf=0.7, verbose=False)
    detection_ocr_2s = sv.Detections.from_ultralytics(result_ocr2s[0])
    print('detection_ocr_1s' , detection_ocr_2s)
    print('no any result because the model is not true')

    boxs_ocr_2 = detection_ocr_2s.xyxy
    conf_ocr_2 = detection_ocr_2s.confidence
    class_id_ocr_2 = detection_ocr_2s.class_id
    print('class-name_ocr2', detection_ocr_2s.data)
    print('class_id_ocr_2', class_id_ocr_2)

    vis.draw_bboxes(frame_ocr2, img_plate, img_plate, boxs_ocr_2 , conf_ocr_2, class_id_ocr_2, obj_class_id, obj_speed, obj_coordinate)

    return
##################################




class Cam2WorldMapper:
    """Maps points from image to world coordinates using perspective transform."""

    def __init__(self) -> None:
        self.M: NDArray | None = None

    def __call__(self, image_pts: ArrayLike) -> NDArray:
        return self.map(image_pts)

    def find_perspective_transform(self, image_pts: ArrayLike, world_pts: ArrayLike) -> NDArray:
        image_pts = np.asarray(image_pts, dtype=np.float32).reshape(-1, 1, 2)
        world_pts = np.asarray(world_pts, dtype=np.float32).reshape(-1, 1, 2)
        self.M = cv.getPerspectiveTransform(image_pts, world_pts)
        return self.M

    def map(self, image_pts: ArrayLike) -> NDArray:
        if self.M is None:
            raise ValueError("Perspective transform not estimated")
        image_pts = np.asarray(image_pts, dtype=np.float32).reshape(-1, 1, 2)
        return cv.perspectiveTransform(image_pts, self.M).reshape(-1, 2)




class PointMarker:
    """Mark points on an image using Left Mouse Button click."""

    def __init__(self, window: str = "Image") -> None:
        self._window = window
        self._points: list[tuple[int, int]] = list()

    def __call__(self, image: NDArray, inplace: bool = False) -> list[tuple[int, int]]:
        return self.mark(image, inplace)

    @property
    def points(self) -> list[tuple[int, int]]:
        return self._points

    def mark(self, image: NDArray, inplace: bool = False) -> list[tuple[int, int]]:
        if not inplace:
            image = image.copy()
        cv.namedWindow(self._window, cv.WINDOW_NORMAL)
        cv.setMouseCallback(self._window, self._record_point, param=image)

        while True:
            cv.imshow(self._window, image)
            if cv.waitKey(1) == ord("q"):
                break

        cv.destroyAllWindows()
        return self._points

    def _record_point(self, event: int, x: int, y: int, flags: int, image: Any | None) -> None:
        if event == cv.EVENT_LBUTTONDOWN:
            self._points.append((x, y))
            if image is not None:
                self._draw_point(image, (x, y))

    def _draw_point(self, image: NDArray, point: tuple[int, int]) -> None:
        cv.drawMarker(image, point, (0, 123, 255), cv.MARKER_CROSS, 20, 4, cv.LINE_AA)




MPS_TO_KPH = 3.6


class Speedometer:
    """Estimates speed of objects in the world coordinates."""

    def __init__(self, mapper: Cam2WorldMapper, fps: int, unit: float = MPS_TO_KPH) -> None:
        self._mapper = mapper
        self._fps = fps
        self._unit = unit
        self._speeds: defaultdict[int, list[int]] = defaultdict(list)

    @property
    def speeds(self) -> defaultdict[int, list[int]]:
        return self._speeds

    def update_with_trace(self, idx: int, image_trace: NDArray) -> None:
        if len(image_trace) > 1:
            world_trace = self._mapper(image_trace)
            # Median displacement in x and y directions.
            # This stabilises after around several frames.
            dx, dy = np.median(np.abs(np.diff(world_trace, axis=0)), axis=0)
            ds = np.linalg.norm((dx, dy))
            self._speeds[idx].append(int(ds * self._fps * self._unit))

    def get_current_speed(self, idx: int) -> int:
        return self._speeds[idx][-1] if self._speeds[idx] else 0






if __name__ == '__main__':
    cb = PointMarker()
    

#cap = cv.VideoCapture(SOURCE_VIDEO)

#ret, frame = cap.read()






cb.mark(imS)
pointers=cb.points
print(pointers)

img=imS

img = cv.cvtColor(cv.cvtColor(img, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2BGR)

color1 = sv.Color.from_hex("#004080")
color2 = sv.Color.from_hex("#f78923")
font = cv.FONT_HERSHEY_SIMPLEX
poly = np.array(pointers)
print(poly[0])
print(pointers[0])


img = sv.draw_filled_polygon(img, poly, color1, 0.5)
img = sv.draw_polygon(img, poly, sv.Color.WHITE, 12)


img = cv.putText(img, 'A', pointers[0], font, 3, (0, 0, 255) , 4, cv.LINE_AA)
img = cv.putText(img, 'B', pointers[1], font, 3, (0, 0, 255) , 4, cv.LINE_AA)
img = cv.putText(img, 'C', pointers[2], font, 3, (0, 0, 255) , 4, cv.LINE_AA)
img = cv.putText(img, 'D', pointers[3], font, 3, (0, 0, 255) , 4, cv.LINE_AA)



imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))

# A, B, C, D previously found in the image.
image_pts = pointers
# M6 is roughly 32 meters wide and 140 meters long there.
world_pts = [(0, 0), (32, 0), (32, 170), (0,70)] 

mapper = Cam2WorldMapper()
mapper.find_perspective_transform(image_pts, world_pts)






# Custom color palette for object tracking.
colors = ("#007fff", "#0072e6", "#0066cc", "#0059b3", "#008799", "#004080", "#003366", "#00264d")
color_palette = sv.ColorPalette(list(map(sv.Color.from_hex, colors)))

# The supervision VideoInfo provides some metadata about the video.
#video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO)
#FPS = video_info.fps
#FPS = FPS#**************************

# Polygonal zone that masks out detected objects that are outside it.
poly = np.array([(0, 410), (1920, 410), (1920, 900), (0, 900)])
zone = sv.PolygonZone(poly, (sv.Position.TOP_CENTER, sv.Position.BOTTOM_CENTER))

bbox_annotator = sv.BoxAnnotator(
    color=color_palette,
    thickness=2,
    color_lookup=sv.ColorLookup.TRACK,
)
trace_annotator = sv.TraceAnnotator(
    color=color_palette,
    position=sv.Position.CENTER,
    thickness=2,
)
label_annotator = sv.RichLabelAnnotator(
    color=color_palette,
    border_radius=2,
    font_size=16,
    color_lookup=sv.ColorLookup.TRACK,
    text_padding=6,
)


print(mapper.M)




print(1)



##############################visulization##########################
cls_dict = get_cls_dict('farsi')
cls_dict3 = get_cls_dict3('farsi3')

vis = BBoxVisualization(cls_dict)
vis3 = BBoxVisualization3(cls_dict3)

#######################

#output_video = "m6-motorway-annotated.mp4"
#width, height = video_info.resolution_wh  # Inferenced image size
# YOLO expects the image size to be a multiple of 32
width = camera1.Width.GetValue()
height = camera1.Height.GetValue()
width, height = round(width / 32) * 32, round(height / 32) * 32
classes = [2, 5, 7]  # Car, Bus, Truck
conf = 0.4  # Detetion confidence threshold

speedometer = Speedometer(mapper, FPS)
print('width',width)
print('height', height)


#########################models####################
#yolo = YOLO("models/yolo11m_obj_detect.pt", task="detect")
#yolo.export(format="engine", imgsz=(height, width), int8=True)  # creates 'yolo11n.onnx'
tensorrt_model = YOLO("models/yolo11m_obj_detect.engine")

####
#model_plates = YOLO("plate_2c_yolo11m.pt" , task="detect")
#model_plates.export(format='engine',  int8=True)
tensorrt_model_plate = YOLO("plate_2c_yolo11m.engine")

#####
#yolo.export(format='engine')#onnx for cpu
#model_ocr1 = YOLO("models/ocr1_dataset_yolo11x.pt" , task="detect")#later replace with true model
#model_ocr1.export(format='engine', int8=True)
trt_model_ocr1 = YOLO("models/ocr1_dataset_yolo11x.engine") 


###########
#model_ocr2 = YOLO("models/ocr_2_yolo11l.pt" , task="detect")#later replace with true model
#model_ocr2.export(format='engine',int8=True) #                    imgsz
trt_model_ocr2 = YOLO("models/ocr_2_yolo11l.engine")

#########################



#####################START##################################
try:
    # Get the transport layer factory
    tl_factory = pylon.TlFactory.GetInstance()

    # Get a list of all available devices
    devices = tl_factory.EnumerateDevices()
    
    if not devices:
        raise pylon.RuntimeException("No camera found.")
    
    # Create InstantCamera objects for the first two devices
    #camera1 = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
    #camera2 = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))
    
    # Open the cameras
    #camera1.Open() #before opened
    #camera1.Width.Value = camera1.Width.Max
    #camera1.Height.Value = camera1.Height.Max
    # YOLO expects the image size to be a multiple of 32
    width = camera1.Width.GetValue()
    height = camera1.Height.GetValue()
    width, height = round(width / 32) * 32, round(height / 32) * 32
    
    #camera2.Open() #before opend
    #camera2.Width.Value = camera2.Width.Max
    #camera2.Height.Value = camera2.Height.Max
    
    print('width',width)
    print('height', height)

    # Set pixel format (e.g., to RGB8 for color cameras)
    #camera1.PixelFormat.Value = "Mono8"   #WAS NOT WRITTABLE
    #camera2.PixelFormat,Value = "RGB8"    #WAS NOT WRITTABLE

    # Start grabbing images (continuous grabbing)
    #camera1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    #camera2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    resulting_fps1 = camera1.ResultingFrameRate.GetValue()
    print(f"Resulting Frame Rate: {resulting_fps1} FPS")
    resulting_fps2 = camera2.ResultingFrameRate.GetValue()
    print(f"Resulting Frame Rate: {resulting_fps2} FPS")
           


    while camera1.IsGrabbing() and camera2.IsGrabbing():
        # Retrieve grab results
        grabResult1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        grabResult2 = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult1.GrabSucceeded() and grabResult2.GrabSucceeded():
            # Convert pylon image to OpenCV format
            img1 = grabResult1.Array
            img2 = grabResult2.Array
            frame= img1
            # Display images
            cv.imshow("Camera 1", img1)
            cv.imshow("Camera 2", frame)
            print('check point')
            print('width',width)
            print('height', height)

            ##############################statrt proc###############
            result = tensorrt_model.track(
                frame,
                classes=classes,
                conf=conf,
                imgsz=(height, width),
                persist=True,
                verbose=False,
                tracker="bytetrack.yaml",
            )
            frame2 = frame
        
            detection = sv.Detections.from_ultralytics(result[0])
            # Mask out detections outside the zone.
            
            detection = detection[zone.trigger(detections=detection)]

            trace_ids = detection.tracker_id  # type: ignore
            speeds: list[int] = list()
            labels: list[str] = list()
            print(trace_ids)
            if trace_ids is not None:
                for trace_id in trace_ids:# seepd meter
                    image_trace = trace_annotator.trace.get(trace_id)
                    speedometer.update_with_trace(int(trace_id), image_trace)
                    current_speed = speedometer.get_current_speed(int(trace_id))
                    speeds.append(current_speed)
                    labels.append(f"#{trace_id} {current_speed} km/h")


                frame = cv.cvtColor(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2RGB)
                #imshow(frame)
                frame = bbox_annotator.annotate(frame, detection)  # type: ignore
                print('xyxy', detection.xyxy[0])
                #imshow(frame)
                print(3)
            
                frame = trace_annotator.annotate(frame, detection)  # type: ignore
            
                print('confidence', detection.confidence[0])
                frame = label_annotator.annotate(frame, detection, labels=labels)  # type: ignore
                imshow(frame)
                #sink.write_frame(frame)
                print(f"Number of dimensions: {detection.xyxy.ndim}")
                print('labela', labels)
                d = detection.xyxy.shape[0]
                print('d', d)

                # Get the total number of elements
                print(f"Total number of elements: {detection.xyxy.size}")
                #imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
                #image_arr = numpy.array(frame)
                frame3 = frame2.copy() 
                for number in range(0, d):
                    x1, y1, x2, y2 = map(int , detection.xyxy[number])
                    if 50<y1<500:
                        frame3 = frame2.copy()
                        cv.imshow('frame2', frame2)
                        crop_object = frame[y1:y2, x1:x2]
                        obj_coordinate = x1, y1, x2, y2 # coordinate of objec
                        print('x1, y1, x2, y2 ', obj_coordinate)
                        imshow(cv.cvtColor(crop_object, cv.COLOR_BGR2RGB))
                        print('trace_id', trace_id)
                
                        print('detection1', detection)
                        obj_class_id = detection.class_id[number]
                        print('class_id', detection.class_id[number])
                        obj_speed = speeds[number]
                        print('object_speed', speeds[number])

                        image1 = cv.imread("/home/cv/Desktop/yolo11 opencv/172.jpg", cv.IMREAD_COLOR)#image1 for trst later replace with crop_object
                        #cv.imshow('testplate',image1)
                        result_plates = platedetection(image1 , tensorrt_model_plate)#call find plate from crop_object
                        if result_plates is not None:
                            detection_plates = sv.Detections.from_ultralytics(result_plates[0])
                            num_of_plates = detection_plates.xyxy.shape[0]
                    
                            print('num_of_plate', num_of_plates)
                            for number in range(0, num_of_plates):# loop crop plates and call ocr
                                x1_p, y1_p, x2_p, y2_p = map(int , detection_plates.xyxy[number])
                                img_plate = image1[y1_p:y2_p, x1_p:x2_p] #img_plate = crop_object[y1_p:y2_p, x1_p:x2_p]
                                class_id_plates = detection_plates.class_id[number]
                                print('class_id_plates', class_id_plates)
                                if class_id_plates == 1 :
                                    print('call- function ocr 1 ') 
                                    frame_ocr1 = frame3
                                    cv.imshow('frame_ocr1' , frame_ocr1)
                                    ocr_1(frame_ocr1,img_plate, obj_class_id ,obj_speed, obj_coordinate, trt_model_ocr1) 
                                if class_id_plates == 0 :
                                    print('call- function ocr 2 ')  
                                    frame_ocr2 = frame3
                                    cv.imshow('frame_ocr2' , frame_ocr2)

                                    ocr_2(frame_ocr2,img_plate, obj_class_id ,obj_speed, obj_coordinate, trt_model_ocr2) 







        # Release the grab results
        grabResult1.Release()
        grabResult2.Release()
    
        # Exit on 'q' key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

          

except pylon.RuntimeException as e:
    print("An error occurred: ", e)

finally:
    # Stop grabbing and close cameras
    if 'camera1' in locals() and camera1.IsOpen():
        camera1.StopGrabbing()
        camera1.Close()
    if 'camera2' in locals() and camera2.IsOpen():
        camera2.StopGrabbing()
        camera2.Close()
    cv.destroyAllWindows()