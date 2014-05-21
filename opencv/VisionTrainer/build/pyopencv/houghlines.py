#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
# This is a standalone program. Pass an image name as a first parameter of the program.

import sys
from math import sin, cos, sqrt
from pyopencv import *

# toggle between CV_HOUGH_STANDARD and CV_HOUGH_PROBILISTIC
USE_STANDARD=0

if __name__ == "__main__":
    filename = "building.jpg"
    if len(sys.argv)>1:
        filename = sys.argv[1]

    src=imread(filename, 0)
    if src.empty():
        print("Error opening image %s" % filename)
        sys.exit(-1)

    dst = Mat(src.size(), CV_8UC1)
    color_dst = Mat(src.size(), CV_8UC3)
    lines = 0
    Canny( src, dst, 50, 200, 3 )
    cvtColor( dst, color_dst, CV_GRAY2BGR )

    if USE_STANDARD:
        lines = HoughLines( dst, 1, CV_PI/180, 100, 0, 0 )

        for i in range(min(len(lines), 100)):
            l = lines[i]
            rho = l[0]
            theta = l[1]
            a = cos(theta)
            b = sin(theta)
            x0 = a*rho 
            y0 = b*rho
            pt1 = Point(round(x0 + 1000*(-b)), round(y0 + 1000*(a)))
            pt2 = Point(round(x0 - 1000*(-b)), round(y0 - 1000*(a)))
            line( color_dst, pt1, pt2, CV_RGB(255,0,0), 3, 8 )

    else:
        lines = HoughLinesP( dst, 1, CV_PI/180, 50, 50, 10 )
        for l in lines:
            line( color_dst, Point(int(l[0]), int(l[1])), 
                Point(int(l[2]), int(l[3])), CV_RGB(255,0,0), 3, 8 )

    namedWindow( "Source", 1 )
    imshow( "Source", src )

    namedWindow( "Hough", 1 )
    imshow( "Hough", color_dst )

    waitKey(0)
