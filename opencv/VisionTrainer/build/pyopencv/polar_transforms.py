#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
import sys
from pyopencv import *


if __name__ == "__main__":
    
    log_polar_img = None
    lin_polar_img = None
    recovered_img = None

    if len(sys.argv)==1:
        capture = VideoCapture( 0 )
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        capture = VideoCapture( int(sys.argv[1]) )
    elif len(sys.argv)==2:
        capture = VideoCapture( sys.argv[1] );

    if not capture.isOpened():
        print("Could not initialize capturing...")
        print("Usage: %s <CAMERA_NUMBER>    , or \n       %s <VIDEO_FILE>\n" % (sys.argv[0],sys.argv[0]))
        sys.exit(-1)
        
    frame = Mat()
        
    namedWindow( "Linear-Polar", 0 )
    namedWindow( "Log-Polar", 0 )
    namedWindow( "Recovered image", 0 )

    moveWindow( "Linear-Polar", 20,20 )
    moveWindow( "Log-Polar", 700,20 )
    moveWindow( "Recovered image", 20,700 )

    while True:
        capture >> frame
        if frame.empty():
            break
            
        if log_polar_img is None:
            log_polar_img = Mat(frame.size(), CV_MAKETYPE(CV_8U, frame.channels()))
            lin_polar_img = Mat(frame.size(), CV_MAKETYPE(CV_8U, frame.channels()))
            recovered_img = Mat(frame.size(), CV_MAKETYPE(CV_8U, frame.channels()))

        pt0 = Point2f(0.5*frame.cols, 0.5*frame.rows)
        logPolar(frame,log_polar_img,pt0,70, INTER_LINEAR+CV_WARP_FILL_OUTLIERS)
        linearPolar(frame,lin_polar_img,pt0,70, INTER_LINEAR+CV_WARP_FILL_OUTLIERS)

        if False: # change this to True to see a different effect
            logPolar(log_polar_img,recovered_img,pt0,70, CV_WARP_INVERSE_MAP+INTER_LINEAR)
        else:
            linearPolar(lin_polar_img,recovered_img,pt0,70, CV_WARP_INVERSE_MAP+INTER_LINEAR+CV_WARP_FILL_OUTLIERS)

        imshow("Log-Polar", log_polar_img );
        imshow("Linear-Polar", lin_polar_img );
        imshow("Recovered image", recovered_img );

        if waitKey(10) >= 0:
            break
