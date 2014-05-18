#!/usr/bin/env python

import sys
import os
import cv2

if len(sys.argv) != 2:
    print "This script requires the video file as its only arguement!"

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)


video_file = sys.argv[1]

video_in = cv2.CaptureVideo(video_file)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

t_minus = cv2.cvtColor(video_in.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(video_in.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(video_in.read()[1], cv2.COLOR_RGB2GRAY)

while True:
    diffimage = diffImg(t_minus, t, t_plus) 
    cv2.imshow(winName, diffimage)
    
    

    # Read next image
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(video_in.read()[1], cv2.COLOR_RGB2GRAY)

    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break


