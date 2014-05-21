#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
from pyopencv import *
import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    im = imread(filename, CV_LOAD_IMAGE_GRAYSCALE)
    im3 = imread(filename, CV_LOAD_IMAGE_COLOR)
    chessboard_dim = Size( 7, 5 )
    
    found, corners = findChessboardCorners( im, chessboard_dim )
    drawChessboardCorners( im3, chessboard_dim, asMat(corners), found )
    
    imshow("win", im3)
    waitKey()
