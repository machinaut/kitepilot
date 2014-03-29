#!/usr/bin/env python
import cv2
import numpy as np
import datetime

# Run at VGA resolution
webcam = cv2.VideoCapture(1)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)

# output window
cv2.namedWindow('foo')

# testing with a mandarin orange
color_min = np.array([7,50,50], np.uint8)
color_max = np.array([12,255,255], np.uint8)

# Measure time for science!
past = datetime.datetime.now()

# loop until forever
while True:
    # time how long a cycle takes
    current = datetime.datetime.now()
    diff = current - past
    print "FPS:", 1.0/(diff.seconds + diff.microseconds*1E-6)
    past = current

    # capture image from camera
    rv,img = webcam.read()
    if not rv:
        print "ERROR capturing image"
        exit(1)

    # TODO: this may be overkill on the blur
    cv2.GaussianBlur(img,(21,21),0)

    # Convert to HSV before threshold
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold within csv
    thresh = cv2.inRange(hsv, color_min, color_max)

    # Show the result
    cv2.imshow('foo', thresh)
