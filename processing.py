import cv2
import numpy as nmp
from time import sleep

capture=cv2.VideoCapture('./demo4.mp4')

frame_nmr = 0
while frame_nmr < 100:
    sleep(1)
    frame_nmr += 1
    
    res, frame = capture.read()
    if res:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res, frame = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
        _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 15)

        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        bgr = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        cv2.imshow('blurred', bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()