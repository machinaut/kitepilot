#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
from pyopencv import *
import numpy.random as NR
import sys

marker_mask = None
markers = None
img0 = None
img = None
img_gray = None 
wshed = None
prev_pt = Point(-1,-1)

def on_mouse( event, x, y, flags, param ):
    global prev_pt
    if img.empty():
        return;
    if( event == CV_EVENT_LBUTTONUP or not (flags & CV_EVENT_FLAG_LBUTTON) ):
        prev_pt = Point(-1,-1)
    elif( event == CV_EVENT_LBUTTONDOWN ):
        prev_pt = Point(x,y)
    elif( event == CV_EVENT_MOUSEMOVE and (flags & CV_EVENT_FLAG_LBUTTON) ):
        pt = Point(x,y)
        if prev_pt.x < 0:
            prev_pt = pt
        line( marker_mask, prev_pt, pt, Scalar.all(255), 5, 8, 0 )
        line( img, prev_pt, pt, Scalar.all(255), 5, 8, 0 )
        prev_pt = pt
        imshow( "image", img )

if __name__ == "__main__":
    filename = "fruits.jpg"
    if len(sys.argv)>1:
        filename = sys.argv[1]

    img0 = imread(filename,1)
    if img0.empty():
        print("Error opening image '%s'" % filename)
        sys.exit(-1)

    print("Hot keys:")
    print("\tESC - quit the program")
    print("\tr - restore the original image")
    print("\tw - run watershed algorithm")
    print("\t  (before that, roughly outline several markers on the image)")

    namedWindow( "image", 1 )
    namedWindow( "watershed transform", 1 )

    img = img0.clone()
    img_gray = img0.clone()
    wshed = img0.clone()
    marker_mask = Mat(img.size(), CV_8UC1)
    markers = Mat(img.size(), CV_32SC1, Scalar())
    markers2 = Mat(img.size(), CV_8UC1)

    # color table for LUT
    color_tab = asMat((NR.rand(1, 256, 3)*180+50).astype('uint8'))

    cvtColor( img, marker_mask, CV_BGR2GRAY )
    cvtColor( marker_mask, img_gray, CV_GRAY2BGR )

    marker_mask.setTo(0)
    wshed.setTo(0)

    imshow( "image", img )
    imshow( "watershed transform", wshed )

    setMouseCallback( "image", on_mouse )
    while True:
        c = '%c' % (waitKey(0) & 255)
        if c=='\x1b':
            break;
        elif c == 'r':
            marker_mask.setTo(0)
            markers.setTo(0)
            img0.copyTo(img)
            imshow( "image", img )
        elif c == 'w':
            contours, hierarchy = findContours(marker_mask, mode=RETR_CCOMP, method=CHAIN_APPROX_SIMPLE)
            comp_count = 0
            idx = 0
            while idx >= 0:
                # there's a bug with not specifying maxLevel
                drawContours( markers, contours, idx, comp_count+1, CV_FILLED, 8, hierarchy, 0 )
                idx = int(hierarchy[idx][0])
                comp_count += 1
                
            t = getTickCount()
            watershed( img0, markers )
            t = getTickCount() - t
            print("exec time = %lf" % (t/(getTickFrequency()*1000.)))

            wshed.setTo(Scalar.all(255))

            # paint the watershed image
            markers.convertTo(markers2, CV_8UC1)
            cvtColor( markers2, wshed, CV_GRAY2BGR )
            LUT(wshed, color_tab, wshed)

            addWeighted( wshed, 0.5, img_gray, 0.5, 0, wshed )
            imshow( "watershed transform", wshed )
