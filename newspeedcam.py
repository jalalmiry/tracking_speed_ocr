import cv2

from ultralytics import solutions






cap = cv2.VideoCapture("/home/cv/Desktop/yolo11 opencv/m6-motorway-annotated-comp.mp4")
assert cap.isOpened(), "Error reading video file"

# Video writer
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("speed_management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize speed estimation object
speedestimator = solutions.SpeedEstimator(
    show=True,  # display the output
    model="models/yolo11n.engine",  # path to the YOLO11 model file.
    fps=fps,  # adjust speed based on frame per second
    # max_speed=120,  # cap speed to a max value (km/h) to avoid outliers
    max_hist=5,  # minimum frames object tracked before computing speed
    # meter_per_pixel=0.05,  # highly depends on the camera configuration
    classes=[2, 5, 7],  # estimate speed of specific classes.classes = [2, 5, 7]  # Car, Bus, Truck
    # line_width=2,  # adjust the line width for bounding boxes
)

# Process video
while cap.isOpened():
    success, im0 = cap.read()

    if not success:
        print("Video frame is empty or processing is complete.")
        break

    results = speedestimator(im0)


    results = speedestimator(im0)
    if speedestimator.track_data.id is not None:
        boxes = speedestimator.track_data.xywh.tolist()  # Bounding boxes
        clss = speedestimator.track_data.cls.cpu().tolist()  # Classes Indexes
        tids = speedestimator.track_data.id.int().cpu().tolist()  # Track ids
        speeds = speedestimator.spd  # Speeds
        
        for tid, box, cls in zip(tids, boxes, clss):
            print(f"ID: {tid}, box: {box}, speed {speeds.get(tid)}, class {speedestimator.names[cls]}")
            box_int = [int(x) for x in box]#convert float to int
            
            box_int.append([speeds.get(tid)])
            box_int.append(speedestimator.names[cls])

            box_speed_clss_string = [str(x) for x in box_int]#convert int to string
            box_speed_clss = ', '.join(map(str, box_speed_clss_string))
            print('box_speed_clss',box_speed_clss)
            print('boxspeedclss_string=',box_speed_clss_string) 

            cv2.imwrite(box_speed_clss + ".jpg" ,im0)
        

    
cap.release()
video_writer.release()
cv2.destroyAllWindows()  # destroy all opened windows