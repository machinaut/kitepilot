#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
from pyopencv import *
from ctypes import c_int
import sys

if __name__ == "__main__":
    img = Mat()
    if len(sys.argv) > 1:
        img = imread(sys.argv[1])
        
    if img.empty():
        print( "ERROR: no image was specified\n" if len(sys.argv) == 1 else "ERROR: the specified image could not be loaded\n")
        print( "Usage: peopledetect <inputimage>\n" )
        sys.exit(-1)

    hog = HOGDescriptor()
    hog.setSVMDetector(HOGDescriptor.getDefaultPeopleDetector())
    t = getTickCount()
    # run the detector with default parameters. to get a higher hit-rate
    # (and more false alarms, respectively), decrease the hitThreshold and
    # groupThreshold (set groupThreshold to 0 to turn off the grouping completely).
    found = hog.detectMultiScale(img, 0, Size(8,8), Size(24,16), 1.05, 2)
    t = float(getTickCount()) - t
    print("Detection time = %gms\n" % (t*1000./getTickFrequency()))
    for r in found:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        r.x += round(r.width*0.1)
        r.y += round(r.height*0.1)
        r.width = round(r.width*0.8)
        r.height = round(r.height*0.8)
        rectangle(img, r.tl(), r.br(), Scalar(0,255,0), 1)

    namedWindow("people detector", 1)
    imshow("people detector", img)
    waitKey(0)
