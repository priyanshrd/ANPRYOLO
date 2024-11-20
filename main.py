from PIL import Image
from ultralytics import YOLO
import cv2
import numpy as np

import util
from sort.sort import *
from util import get_car, write_csv, read_license_plate

results = {}

mot_tracker = Sort()

# Load models
coco_model = YOLO('yolov8x.pt')  # YOLO model for cars
license_plate_detector = YOLO("runs/detect/train17/weights/best.pt")

# Load video
cap = cv2.VideoCapture('demo9')  # PATH_TO_THE_VIDEO

vehicles = [2, 3, 5, 7]  # Car, motorbike, bus, or truck in YOLO

# Read frames
frame_nmr = 0
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}

        # Detect vehicles
        detections = coco_model(frame)[0]
        detections_ = [[0, 0, 0, 0, 0]]
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if not (x1 is None or x2 is None or y1 is None or y2 is None):
                if int(class_id) in vehicles:  # If it's a vehicle
                    detections_.append([x1, y1, x2, y2, score])  # Storing bounding boxes

        track_ids = mot_tracker.update(np.asarray(detections_))  # Tracking vehicles

        # Detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # Assign license plate to car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:
                # Crop license plate to send it to OCR
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                # Image process license plate for compatible OCR
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 100, 255, cv2.THRESH_BINARY_INV)

                # Read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {
                        'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},  # Where the car is located
                        'license_plate': {
                            'bbox': [x1, y1, x2, y2],  # Where the license plate is located
                            'text': license_plate_text,
                            'bbox_score': score,
                            'text_score': license_plate_text_score
                        }
                    }

                    # Draw bounding boxes and text on the frame
                    # Draw the car bounding box
                    cv2.rectangle(frame, (int(xcar1), int(ycar1)), (int(xcar2), int(ycar2)), (0, 255, 0), 2)
                    # Draw the license plate bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                    # Put the license plate text near the bounding box
                    cv2.putText(frame, license_plate_text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()

# Write results
write_csv(results, './testdemo9_2.csv') #FILE_TO_SAVE_RESULTS
