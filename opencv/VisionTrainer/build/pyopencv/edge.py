#!/usr/bin/env python
# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv

print("OpenCV Python version of edge")

import sys

# import the necessary things for OpenCV
from pyopencv import *

# some definitions
win_name = "Edge"
trackbar_name = "Threshold"

# the callback on the trackbar
def on_trackbar (position, param):
    smooth (gray, edge, CV_BLUR, 3, 3, 0)
    bitwise_not (gray, edge)

    # run the edge dector on gray scale
    Canny (gray, edge, position, position * 3, 3)

    # reset
    col_edge[:] = 0

    # copy edge points
    image.copyTo(col_edge, edge)
    
    # show the image
    imshow (win_name, col_edge)

if __name__ == '__main__':
    filename = "fruits.jpg"

    if len(sys.argv)>1:
        filename = sys.argv[1]

    # load the image gived on the command line
    image = imread (filename)

    if not image:
        print("Error loading image '%s'" % filename)
        sys.exit(-1)

    # create the output image
    col_edge = Mat(image.size(), CV_8UC3)

    # convert to grayscale
    gray = Mat(image.size(), CV_8UC1)
    edge = Mat(image.size(), CV_8UC1)
    cvtColor (image, gray, CV_BGR2GRAY)

    # create the window
    namedWindow (win_name, CV_WINDOW_AUTOSIZE)

    # create the trackbar
    createTrackbar (trackbar_name, win_name, 1, 100, on_trackbar)

    # show the image
    on_trackbar (0, None)

    # wait a key pressed to end
    waitKey(0)
