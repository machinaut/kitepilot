#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
from pyopencv import *
import sys

if __name__ == "__main__":
    laplace = None
    colorlaplace = None
    planes = None
    capture = None
    
    if len(sys.argv)==1:
        capture = VideoCapture( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = VideoCapture( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        capture = VideoCapture( sys.argv[1] ); 

    if not capture.isOpened():
        print("Could not initialize capturing...")
        sys.exit(-1)
        
    namedWindow( "Laplacian", CV_WINDOW_AUTOSIZE )
    frame = Mat()
    planes = vector_Mat()

    while True:
        capture >> frame
        if frame.empty():
            break
            
        if not laplace:
            laplace = Mat(frame.size(), CV_16SC1)
            colorlaplace = Mat(frame.size(), CV_8UC3)

        split( frame, planes )
        for plane in planes:
            Laplacian( plane, laplace, 3 )
            convertScaleAbs( laplace, plane, 1, 0 )

        merge( planes, colorlaplace )

        imshow("Laplacian", colorlaplace )

        if waitKey(1) > 0:
            break
