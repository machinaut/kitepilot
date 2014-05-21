#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
import sys
import pyopencv as cv
import numpy as np

src = None
image = None
dest = None
element = None

def Opening(pos, user_data):
    element = cv.asMat(np.ones((pos*2+1, pos*2+1), 'uint8'), True)
    cv.erode(src, image, element)
    cv.dilate(image, dest, element)
    cv.imshow("Opening&Closing window",dest);
def Closing(pos, user_data):
    element = cv.asMat(np.ones((pos*2+1, pos*2+1), 'uint8'), True)
    cv.dilate(src, image, element)
    cv.erode(image, dest, element)
    cv.imshow("Opening&Closing window",dest);
def Erosion(pos, user_data):
    element = cv.asMat(np.ones((pos*2+1, pos*2+1), 'uint8'), True)
    cv.erode(src, dest, element)
    cv.imshow("Erosion&Dilation window",dest);
def Dilation(pos, user_data):
    element = cv.asMat(np.ones((pos*2+1, pos*2+1), 'uint8'), True)
    cv.dilate(src, dest, element)
    cv.imshow("Erosion&Dilation window",dest);

if __name__ == "__main__":
    filename = "baboon.jpg"
    if len(sys.argv)==2:
        filename = sys.argv[1]
    src = cv.imread(filename,1)
    if src.empty():
        sys.exit(-1)
    image = src.clone()
    dest = src.clone()
    cv.namedWindow("Opening&Closing window",1)
    cv.namedWindow("Erosion&Dilation window",1)
    cv.imshow("Opening&Closing window",src)
    cv.imshow("Erosion&Dilation window",src)
    cv.createTrackbar("Open","Opening&Closing window",0,10,Opening)
    cv.createTrackbar("Close","Opening&Closing window",0,10,Closing)
    cv.createTrackbar("Dilate","Erosion&Dilation window",0,10,Dilation)
    cv.createTrackbar("Erode","Erosion&Dilation window",0,10,Erosion)
    cv.waitKey(0)
    
