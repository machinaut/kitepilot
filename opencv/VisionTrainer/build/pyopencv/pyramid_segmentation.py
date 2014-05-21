#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
import sys
from pyopencv import *
from ctypes import c_int
image0 = None
image1 = None
level = 4
block_size = 1000
storage = None

def ON_SEGMENT(pos, param):
    comp = pyrSegmentation(image0, image1, storage, level, threshold1.value+1, threshold2.value+1)
    imshow("Segmentation", image1)

if __name__ == "__main__":
    filename = "fruits.jpg";
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    image = imread( filename, 1)
    if image.empty():
        print("Error opening %s" % filename)
        sys.exit(-1)

    namedWindow("Source", 0)
    imshow("Source", image)
    namedWindow("Segmentation", 0)
    storage = createMemStorage ( block_size )
    image.cols &= -(1<<level)
    image.rows &= -(1<<level)
    image0 = image.clone()
    image1 = image.clone()
    # segmentation of the color image
    l = 1
    threshold1 = c_int(255)
    threshold2 = c_int(30)
    ON_SEGMENT(1, None)
    sthreshold1 = createTrackbar("Threshold1", "Segmentation", threshold1, 255, ON_SEGMENT)
    sthreshold2 = createTrackbar("Threshold2", "Segmentation",  threshold2, 255, ON_SEGMENT)
    imshow("Segmentation", image1)
    waitKey(0)
