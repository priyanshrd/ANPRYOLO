from PIL import Image
from ultralytics import YOLO
import cv2

import util
from sort.sort import *
from util import get_car, write_csv, read_license_plate


results = {}

mot_tracker = Sort()

# load models
coco_model = YOLO('yolov8x.pt')   #YOlo model for cars
license_plate_detector = YOLO("runs/detect/train17/weights/best.pt")
# load video
cap = cv2.VideoCapture('WhatsApp Image 2024-01-01 at 16.45.08_938d3997.jpg')

vehicles = [2, 3, 5, 7]   #  Car motorbike bus or truck in yolo





# read frames
frame_nmr = 0
ret = True
while ret:                  #Reading each frame of video
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}
                                            # detect vehicles
        detections = coco_model(frame)[0]    
        detections_ = [[0,0,0,0,0]]
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if not(x1==None or x2==None or y1==None or y2==None):
                if int(class_id) in vehicles:                       #if its a vehicle
                    detections_.append([x1, y1, x2, y2, score])     #storing bounding boxes

        
        track_ids = mot_tracker.update(np.asarray(detections_))        #tracking vehicles giving their bounding boxes and vehicle id

        
        # detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            
            x1, y1, x2, y2, score, class_id = license_plate

            # assign license plate to car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:

                
                # crop license plate to send it to OCR
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                
                
                # image process license plate for compatible OCR
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 100, 255, cv2.THRESH_BINARY_INV)


                # read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},     #WHERE CAR IS LOCATED
                                                  'license_plate': {'bbox': [x1, y1, x2, y2],     # where licence plate located
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': license_plate_text_score
                                                                    }}
    else:
        break

# write results
write_csv(results, './testdemo9_2.csv')