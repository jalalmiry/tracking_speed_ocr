import cv2

from ultralytics import solutions





cap = cv2.VideoCapture("/home/cv/Desktop/yolo11 opencv/m6-motorway-annotated-comp.mp4")
assert cap.isOpened(), "Error reading video file"

# Video writer
w, h = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
#video_writer = cv2.VideoWriter("speed_management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
fps = float(cap.get(cv2.CAP_PROP_FPS))
# Initialize speed estimation object
se = solutions.SpeedEstimator(
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
    ok, im0 = cap.read()
    if not ok:
        break

    img_color=im0.copy()
    _ = se(im0)  # call once per frame
    
    if not se.track_ids:
        continue

    for box, tid, cls in zip(se.boxes, se.track_ids, se.clss):  # boxes are xyxy
        if tid not in se.locked_ids:
            continue  # skip until speed is locked
        spd = se.spd.get(tid)
        x1, y1, x2, y2 = map(int, box.tolist())
        crop = im0[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]  # car crop for LPR
        cv2.imshow('crop_img',crop)
        print(f"id={tid} cls={se.names[cls]} speed={spd} xyxy={(x1,y1,x2,y2)}")
        # run LPR on 'crop' here
        ######################conver-int to string for name of image###############
        box_speed_clss = [x1,y1,x2,y2]
        box_speed_clss.append([spd])
        box_speed_clss = [str(x) for x in box_speed_clss]#convert int to string
        box_speed_clss.append([se.names[cls]])
        box_speed_clss = ', '.join(map(str, box_speed_clss))
        print(box_speed_clss)
        
        
        #######################################concatrring################
        horizontal_concat = cv2.hconcat([im0, img_color])
        cv2.imwrite("/home/cv/Desktop/share/" + box_speed_clss + ".jpg" ,horizontal_concat)
        
        #####################convert string to int from name of image
        box_speed_clss = box_speed_clss.split(',')
        cls_after = box_speed_clss.pop(5)
        spd_after = box_speed_clss.pop(4)
        
        box_after = list(map(int, box_speed_clss))
       
        x1=box_after[0]
        y1=box_after[1]
        x2=box_after[2]
        y2=box_after[3]
        
        crop2 = horizontal_concat[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]  # car crop for LPR
        cv2.imshow('crop_img222',crop2)

cap.release()
cv2.destroyAllWindows()