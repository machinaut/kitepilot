#!/usr/bin/env python

# Minh-Tri's demo of using DifferentialImage to compute curvature
from pyopencv import *
import sys

if __name__ == "__main__":
    if len(sys.argv)==2:
        frame = imread(sys.argv[1], CV_LOAD_IMAGE_COLOR)
    else:
        frame = imread('ellipses.png', CV_LOAD_IMAGE_COLOR)

    if frame.empty():
        print("Could not load image...")
        sys.exit(-1)
        
    namedWindow( "Video", CV_WINDOW_AUTOSIZE )
    namedWindow( "Curvature", CV_WINDOW_AUTOSIZE )
    
    di = DifferentialImage(ksize=15)

    frame_gray = Mat(frame.size(), CV_8UC1)
    curvature = Mat(frame.size(), CV_64FC1)
    out_curvature = Mat(frame.size(), CV_8UC1)
        
    cvtColor(frame, frame_gray, CV_BGR2GRAY)
    di(frame_gray)
    di.curvature(curvature)
    absdiff(curvature, Scalar(0), curvature)
    _, vmax, _, _ = minMaxLoc(curvature)
    curvature.convertTo(out_curvature, CV_8UC1, 512/vmax, 0)

    imshow("Video", frame )
    imshow("Curvature", out_curvature )

    waitKey(0)
