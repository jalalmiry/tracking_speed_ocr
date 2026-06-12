"""visulization save image and csv file and bounding boxes


"""


import numpy as np
import cv2
import datetime
import xml.etree.ElementTree as xml
import os
import shutil
from datetime import timedelta, date
import csv 
# Constants
ALPHA = 0.5
FONT = cv2.FONT_HERSHEY_PLAIN
TEXT_SCALE = 1.0
TEXT_THICKNESS = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def gen_colors(num_colors):
    """Generate different colors.

    # Arguments
      num_colors: total number of colors/classes.

    # Output
      bgrs: a list of (B, G, R) tuples which correspond to each of
            the colors/classes.
    """
    import random
    import colorsys

    hsvs = [[float(x) / num_colors, 1., 0.7] for x in range(num_colors)]
    random.seed(1234)
    random.shuffle(hsvs)
    rgbs = list(map(lambda x: list(colorsys.hsv_to_rgb(*x)), hsvs))
    bgrs = [(int(rgb[2] * 255), int(rgb[1] * 255),  int(rgb[0] * 255))
            for rgb in rgbs]
    return bgrs


def draw_boxed_text(img, text, topleft, color):
    """Draw a transluent boxed text in white, overlayed on top of a
    colored patch surrounded by a black border. FONT, TEXT_SCALE,
    TEXT_THICKNESS and ALPHA values are constants (fixed) as defined
    on top.

    # Arguments
      img: the input image as a numpy array.
      text: the text to be drawn.
      topleft: XY coordinate of the topleft corner of the boxed text.
      color: color of the patch, i.e. background of the text.

    # Output
      img: note the original image is modified inplace.
    """
    assert img.dtype == np.uint8
    #print('img.shape',img.shape)
    #for colr plate select img_h, img_w, _ = img.shape  1
    #img_h, img_w, _ = img.shape
    #img_h, img_w = img.shape
    img_h, img_w, _ = img.shape
    if topleft[0] >= img_w or topleft[1] >= img_h:
        return img
    margin = 3
    size = cv2.getTextSize(text, FONT, TEXT_SCALE, TEXT_THICKNESS)
    w = size[0][0] + margin * 2
    h = size[0][1] + margin * 2
    # the patch is used to draw boxed text
    patch = np.zeros((h, w, 3), dtype=np.uint8)
    patch[...] = color
    #cv2.putText(patch, text, (margin+1, h-margin-2), FONT, TEXT_SCALE,
                #WHITE, thickness=TEXT_THICKNESS, lineType=cv2.LINE_8)
    cv2.rectangle(patch, (0, 0), (w-1, h-1), BLACK, thickness=1)
    w = min(w, img_w - topleft[0])  # clip overlay at image boundary
    h = min(h, img_h - topleft[1])
    # Overlay the boxed text onto region of interest (roi) in img
    roi = img[topleft[1]:topleft[1]+h, topleft[0]:topleft[0]+w, :]           # 2
    #roi = img[topleft[1]:topleft[1]+h, topleft[0]:topleft[0]+w]
    #cv2.addWeighted(patch[0:h, 0:w, :], ALPHA, roi, 1 - ALPHA, 0, roi)      #  3
    return img

def create_xml_imwrite(plate_string,img, img_plate, obj_class_id, obj_speed, obj_coordinate, lane):
    plate_final = plate_string
    obj_class_id_str = str(obj_class_id)
    obj_speed_str = str(obj_speed)
    lane_str = str(lane)



    top = xml.Element('TTCC')
    
    child1  = xml.SubElement(top, 'passDateTime')
    child1.text = str(datetime.datetime.now())

    child2 = xml.SubElement(top, 'index')
    child2.text = '0'

    child3 = xml.SubElement(top, 'lineNumber')
    child3.text = '0'

    child4 = xml.SubElement(top, 'vehicleSpeed')
    child4.text = obj_speed_str

    child5 = xml.SubElement(top,'vehiclePlate')
    child5.text = plate_final

    child6 = xml.SubElement(top, 'allowed')
    child6.text = '1'

    child7 = xml.SubElement(top, 'vehicleClass')
    child7.text = obj_class_id_str
    
    child8 = xml.SubElement(top, 'lane')
    child8.text = lane_str

    child9 = xml.SubElement(top,'wrongDirection')
    child9.text = '0'

    child10 = xml.SubElement(top, 'VEHICLELEN')
    child10.text = '0'

    child11 = xml.SubElement(top, 'HEADGAP')
    child11.text = '0'

    child12 = xml.SubElement(top, 'GAP')
    child12.text = '0'
    
    tree = xml.ElementTree(top)
    todayDate = datetime.datetime.now().strftime('%Y-%m-%d')
    hour = datetime.datetime.now().strftime('%H')
    

    

    directory = '/home/cv/Desktop/ttcc/xml/' + todayDate + "/" + hour
    directory2 = "/home/cv/Desktop/ttcc/plate/" + todayDate + "/" + hour
    directory3 = "/home/cv/Desktop/ttcc/image/" + todayDate + "/" + hour
    
    if not os.path.exists(directory):
       os.makedirs(directory)
       with open(directory + '/' + todayDate + '-' + hour + '-' + 'report.csv', 'w') as csvfile:
           filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
           filewriter.writerow(['name', 'plate', 'date', 'class', 'speed', 'lane'])
           

    #tree.write("/home/cv/Desktop/xml/" + plate_final + ".xml")
    tree.write(directory + "/" + plate_final + ".xml")
    #with open(directory + '/report.csv', 'r') as csvread:
        #last_line = csvread.readlines()[-1]
        #second_column = last_line[1]
        
    with open(directory + '/' + todayDate + '-' + hour + '-' + 'report.csv', 'a+', newline='') as csvfile:
            filewriter2 = csv.writer(csvfile)
            filewriter2.writerow(['YADEGAR_MARZDARAN', plate_final, child1.text, obj_class_id_str, obj_speed_str, lane_str])
                
    
    if not os.path.exists(directory2):
       os.makedirs(directory2)
    cv2.imwrite(directory2 + "/" + plate_final + ".jpg", img_plate)

 
    if not os.path.exists(directory3):
       os.makedirs(directory3)
    img_plate_resize = cv2.resize(img_plate, (420, 85))
    h_plate_resize , w_plate_resize, _ = img_plate_resize.shape
    roi = img[10: (h_plate_resize + 10), 10 : (w_plate_resize +10)] 
    result = cv2.addWeighted(roi, 0, img_plate_resize, 1 , 0)
    img[10: (h_plate_resize + 10), 10 : (w_plate_resize +10)] = result
    font = cv2.FONT_HERSHEY_PLAIN
    img = cv2.putText(img, 'TEHRAN TRAFFIC CONTROL', (10,130), font, 3, (0,255,0), 3, cv2.LINE_AA )
    img = cv2.putText(img, plate_final, (10,190), font, 3, (0,255,0), 3, cv2.LINE_AA )
    img = cv2.putText(img, child1.text, (10,240), font, 3, (0,255,0), 3, cv2.LINE_AA )
    x1, y1, x2, y2 = map(int , obj_coordinate)
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (36,255,12), 2)
    img = cv2.putText(img, obj_speed_str, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
    cv2.imwrite(directory3 + "/" + plate_final + ".jpg", img)

    
    seven_days_ago = date.today() - timedelta(days=7)
    olddirectory = '/home/cv/Desktop/ttcc/xml/' + str(seven_days_ago) + "/" + hour
    olddirectory2 = '/home/cv/Desktop/ttcc/plate/' + str(seven_days_ago) + "/" + hour
    olddirectory3 = '/home/cv/Desktop/ttcc/image/' + str(seven_days_ago) + "/" + hour

    print(olddirectory)
    if os.path.exists(olddirectory):
       shutil.rmtree(olddirectory)
    if os.path.exists(olddirectory2):
       shutil.rmtree(olddirectory2)
    if os.path.exists(olddirectory3):
       shutil.rmtree(olddirectory3)      



class BBoxVisualization3():
    """BBoxVisualization class implements nice drawing of boudning boxes.

    # Arguments
      cls_dict: a dictionary used to translate class id to its name.
    """

    def __init__(self, cls_dict):
        self.cls_dict = cls_dict
        self.colors = gen_colors(len(cls_dict))

    def draw_bboxes3(self,img, img_plate, boxes, confs, clss, obj_class_id, obj_speed, obj_coordinate, lane) -> None:
        """Draw detected bounding boxes on the original image."""
        n = len(clss)    
        plate = np.array([[0, 0, 0]])
        for number in range(0, n):
            print('class', number)
            cl = clss[number]
            x_min, y_min, x_max, y_max = map(int , boxes[number])
            color = self.colors[cl]
            cv2.rectangle(img_crop, (x_min, y_min), (x_max, y_max), color, 2)
            txt_loc = (max(x_min+2, 0), max(y_min+2, 0))
            cls_name = self.cls_dict.get(cl, 'CLS{}'.format(cl))
            txt = '{} {:.2f}'.format(cls_name, confs[number])
            print('tet =', txt)
            img = draw_boxed_text(img, txt, txt_loc, color)
            print('cls_name=', cls_name)
            plate = np.append(plate, [[x_min, confs[number], cls_name]], axis = 0)
        plate = np.delete(plate, 0, axis=0)
        #print('plate1=', plate)
        #plate[np.argsort(plate[:,0])]
        plate = plate[plate[:,0].astype(int).argsort()]#sort plate number
        #print('plate1_after_sort=', plate)
        plate = plate[:,2]
        l = len(plate)
        print('length of plate = ', l)
        print('plate Num=', plate)  
        if 6 <= l:
        #if l==8:   
            cv2.imwrite("/home/cv/Desktop/plate." + str(plate) + ".jpg", img) 
            cv2.imwrite("/home/cv/Desktop/plate/" + str(plate) + ".jpg", img)   
            plate_final = str(plate).strip('[]')
            cv2.imwrite("/home/cv/Desktop/record/" + plate_final + ".jpg", img)
            create_xml_imwrite(plate_final, img_color,img, obj_class_id, obj_speed, obj_coordinate, lane)    
        return 
        
    def draw_bboxes2(self, img, boxes, confs, clss):
        """Draw detected bounding boxes on the original image."""
        for bb, cf, cl in zip(boxes, confs, clss):
            cl = int(cl)
            x_min, y_min, x_max, y_max = bb[0], bb[1], bb[2], bb[3]
            color = self.colors[cl+1]
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
            txt_loc = (max(x_min+2, 0), max(y_min+2, 0))
            cls_name = self.cls_dict.get(cl, 'CLS{}'.format(cl))
            txt = '{} {:.2f}'.format(cls_name, cf)
            img = draw_boxed_text(img, txt, txt_loc, color)
        return img
