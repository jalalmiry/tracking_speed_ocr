import cv2
import glob
import os
import numpy as np
from pathlib import Path
import os
from PIL import Image # For image handling (optional, but useful if you want to open/process them)


import gdown
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import supervision as sv
from IPython.display import Video
from numpy.typing import ArrayLike, NDArray
from scipy.signal import savgol_filter
from ultralytics import YOLO


##################visulization###########################################
from utils.classes import get_cls_dict
from utils3.classes3 import get_cls_dict3
from utils.visualization import BBoxVisualization
from utils3.visualization3 import BBoxVisualization3
######################################



##############################visulization##########################
cls_dict = get_cls_dict('farsi')
cls_dict3 = get_cls_dict3('farsi3')

vis = BBoxVisualization(cls_dict)
vis3 = BBoxVisualization3(cls_dict3)

#######################
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


######################OCR_1###d######################
def  ocr_1(img_color, img_plate, obj_class_id ,obj_speed , obj_coordinate, lane, model_ocr1) -> None:
    cv.imshow('before _enhance_plate', img_plate)
    img_plate = cv.bilateralFilter(img_plate, 11, 17, 17) 
    img_plate, alpha, beta = automatic_brightness_and_contrast(img_plate) #enhance plate
    cv.imshow('enhance_plate', img_plate)

    result_ocr1s = model_ocr1(img_plate, conf=0.7, verbose=False)
    detection_ocr_1s = sv.Detections.from_ultralytics(result_ocr1s[0])
    print('detection_ocr_1s' , detection_ocr_1s)
    print('no any result because the model is not true')

    boxs_ocr_1 = detection_ocr_1s.xyxy
    conf_ocr_1 = detection_ocr_1s.confidence
    class_id_ocr_1 = detection_ocr_1s.class_id
    print('class-name_ocr1', detection_ocr_1s.data)
    print('class_id_ocr_1', class_id_ocr_1)

    vis3.draw_bboxes3(img_color, img_plate, boxs_ocr_1 , conf_ocr_1, class_id_ocr_1, obj_class_id, obj_speed, obj_coordinate ,lane)

    return
#################################ocr_2#################################
def  ocr_2(img_color, img_plate, obj_class_id ,obj_speed , obj_coordinate, lane, model_ocr1) -> None:
    cv.imshow('before _enhance_plate', img_plate)
    img_plate = cv.bilateralFilter(img_plate, 11, 17, 17) 
    img_plate, alpha, beta = automatic_brightness_and_contrast(img_plate) #enhance plate
    cv.imshow('enhance_plate', img_plate)

    result_ocr1s = model_ocr1(img_plate, conf=0.7, verbose=False)
    detection_ocr_1s = sv.Detections.from_ultralytics(result_ocr1s[0])
    print('detection_ocr_1s' , detection_ocr_1s)
    print('no any result because the model is not true')

    boxs_ocr_1 = detection_ocr_1s.xyxy
    conf_ocr_1 = detection_ocr_1s.confidence
    class_id_ocr_1 = detection_ocr_1s.class_id
    print('class-name_ocr1', detection_ocr_1s.data)
    print('class_id_ocr_1', class_id_ocr_1)

    vis.draw_bboxes(img_color, img_plate, boxs_ocr_1, conf_ocr_1, class_id_ocr_1, obj_class_id, obj_speed, obj_coordinate, lane)

    return
##################################
####################platedetection#####################
def platedetection(crop_img , onnx_model_plate)-> NDArray:

    result_plates = onnx_model_plate(crop_img,conf=0.7, verbose=False)
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


#########################models####################

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

def find_two_images(folder_path):
    """
    Finds and returns the paths of the first two image files found in a given folder.
    """
    image_files = []
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff') # Add more as needed

    try:
        for filename in os.listdir(folder_path):
            if len(image_files) >= 2:
                break # Stop if two images are already found

            file_path = os.path.join(folder_path, filename)

            # Check if it's a file and has a supported image extension
            if os.path.isfile(file_path) and filename.lower().endswith(supported_extensions):
                image_files.append(file_path)

        return image_files

    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



while True:
    folder_to_scan = "/home/cv/Desktop/share" 
    found_images = find_two_images(folder_to_scan)
    
    if found_images:
        print("Found the following two image files:")
        for img_path in found_images:
            print(img_path)
            img_hconcat = cv2.imread(img_path)
            #cv2.imshow('l' , np.array(img_hconcat, dtype = np.uint8 ) )
            #cv2.imshow('img_hconcat',img_hconcat)
            #cv2.waitKey(0)
            #print('img_orig dtype: %s' % img_hconcat.dtype) 
            ########################extract filene name and convert to int############
            # Get the filename with extension
            file_name_with_ext = os.path.basename(img_path)
            print(f"File name with extension: {file_name_with_ext}")

            # Get the filename without extension
            file_name_without_ext = os.path.splitext(file_name_with_ext)[0]
            print(f"File name without extension: {file_name_without_ext}")
            file_name_without_ext = file_name_without_ext.split(',')
            cls_obj = file_name_without_ext.pop(5)
            spd_obj = file_name_without_ext.pop(4)
        
            box_obj = list(map(int, file_name_without_ext))
       
            x1=box_obj[0]
            y1=box_obj[1]
            x2=box_obj[2]
            y2=box_obj[3]
            ###################cut IR and color images and obj_box and determine lane
            if 5<y1<900:
                height, width = img_hconcat.shape[:2]
                img_IR = img_hconcat[0:1080, 0:1920 ] #cropped_image = image[start_y:end_y, start_x:end_x]
                img_color = img_hconcat[0:1080, 1920:3840]
                img_box = img_IR[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]  # car crop for LPR
                obj_coordinate = x1, y1, x2, y2
                if x1 >= 900 :
                    lane = 1
                elif x1>=600 and x1<=899:
                    lane = 2
                elif x1>=300 and x1<=599:
                    lane_str = 3
                else:
                    lane = 4
            

            ##########################extract plate
                result_plates = platedetection(img_box , tensorrt_model_plate)#call find plate from crop_object
                if result_plates is not None:
                    detection_plates = sv.Detections.from_ultralytics(result_plates[0])
                    num_of_plates = detection_plates.xyxy.shape[0]


                    print('num_of_plate', num_of_plates)
                    for number in range(0, num_of_plates):# loop crop plates and call ocr
                        x1_p, y1_p, x2_p, y2_p = map(int , detection_plates.xyxy[number])
                        img_plate = img_box[y1_p:y2_p, x1_p:x2_p] #img_plate = crop_object[y1_p:y2_p, x1_p:x2_p]
                        class_id_plates = detection_plates.class_id[number]
                     
                        if class_id_plates == 1 :                                  
                            ocr_1(img_color ,img_plate, cls_obj, spd_obj, obj_coordinate,lane, model_ocr1) 
                        
                        if class_id_plates == 0 :
                                                                              
                            ocr_2(img_color  ,img_plate, cls_obj ,spd_obj, obj_coordinate,lane, model_ocr2) 


            #cv2.imshow('IR_IMG=', img_IR)
            #cv2.imshow('crop_img222',img_box)
            #cv2.waitKey(0)
            # You can open and process the images here if needed
            # try:
            #     img = Image.open(img_path)
            #     img.show() # To display the image
            # except Exception as e:
            #     print(f"Could not open image {img_path}: {e}")
            try:
                # Attempt to remove the file
                os.remove(img_path)
                print(f"Image '{img_path}' deleted successfully.")
            except FileNotFoundError:
                print(f"Error: Image '{img_path}' not found.")
            except Exception as e:
                print(f"An error occurred while deleting the image: {e}")
    else:
        print("Could not find two image files in the specified folder.")

    
    #break




