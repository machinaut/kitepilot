#!/usr/bin/env python
import cv2
import numpy as np
import datetime
import glob
import time
from collections import deque

VID_FILE = False

VGA_W = 640
VGA_H = 480

# Run at VGA resolution
webcam = cv2.VideoCapture(0)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,VGA_W)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,VGA_H)

# output window
cv2.namedWindow('foo')

# testing with a green iPhone 5c
color_min = np.array([50,60,60], np.uint8)
color_max = np.array([65,255,255], np.uint8)

# Open a Video File??????
if VID_FILE:
    print glob.glob('~/Downloads/*')
    cap = cv2.VideoCapture('/Users/mike1000/Downloads/KITE.mov')

# Measure time for science!
past = datetime.datetime.now()

# Path History
blob_hist = deque([])

# loop until forever
while True:
    # time how long a cycle takes
    current = datetime.datetime.now()
    diff = current - past
    print "FPS:", 1.0/(diff.seconds + diff.microseconds*1E-6)
    past = current

    # capture image from camera
    if VID_FILE:
        rv, img = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
    else:
        rv, img = webcam.read()

    if not rv:
        print "ERROR capturing image"
        exit(1)

    # TODO: this may be overkill on the blur
    cv2.GaussianBlur(img,(15,15),0)

    # Convert to HSV before threshold
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold within csv
    thresh = cv2.inRange(hsv, color_min, color_max)

    thresh1 = thresh.copy()

    cv2.GaussianBlur(thresh1,(3,3),0)


    # Get the contours...
    #cont = cv2.Canny(thresh, 10, 200)
    #contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_TC89_KCOS)
    
    #print contours
    try:
        cnt = contours[0]
        #cv2.drawContours(thresh, [cnt], 0, (0,255,0), -1)
        #print cnt
        
        M = cv2.moments(cnt)
        #print M
        
        # Get the size of each blob, then sort them by size. This sets the lower
        # bound on the acceptable blob size.
        blobs_with_sizes = [(cv2.contourArea(blob), blob) for blob in contours]
        sorted_blobs = sorted(blobs_with_sizes, key = lambda tup: tup[0], reverse=True)
        
        good_blobs = []
        
        # Only look at the first few blobs...
        for size, blob in sorted_blobs[:5]:
            (x,y),radius = cv2.minEnclosingCircle(blob)
            center = (int(x),int(y))
            radius = int(radius)
            
            if (2*radius) < ( 0.5 * VGA_W ):
                good_blobs.append((size, blob, center, radius))
                cv2.circle(img,center,radius,(0,255,0),2)      
                
        best_size, best_blob, best_center, best_radius = good_blobs[0]
        
        # Calculate our motion vector!!
        try:
            motion = best_center - blob_hist[-1]
            print motion
        except:
            print "First loop... No object history"

        # Add the best point to the history
        blob_hist.append(best_center)
        if len(blob_hist) > 10:
            blob_hist.popleft()
        
        print blob_hist
        
    except Exception, e:
        #raise
        print 'NOPE', e


    # Show the result
    
    cv2.imshow('foo', thresh1)
    cv2.imshow('bar', img)
  
