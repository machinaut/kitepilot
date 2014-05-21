#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
from pyopencv import *
from math import cos, sin

w = 500
levels = 3
contours = None
hierarchy = None

def on_trackbar(pos, param):
    cnt_img = Mat(Size(w, w), CV_8UC3)
    cnt_img.setTo(0)
    
    if pos <= 3:
        h = [x[0] for x in hierarchy]
        idx = int(h[h[h[0]]])
        max_level = 3-pos
    else:
        idx = -1
        max_level = pos-3
    
    drawContours( cnt_img, contours, idx, CV_RGB(255,0,0), CV_FILLED, 8, hierarchy, max_level )
    imshow( "contours", cnt_img )
    
def generate_image():    
    img = Mat(Size(w,w), CV_8UC1)
    img.setTo(0)

    for i in range(6):
        dx = (i%2)*250 - 30
        dy = (i/2)*150
        white = Scalar(255)
        black = Scalar(0)

        if i==0:
            for j in range(11):
                angle = (j+5)*CV_PI/21
                line(img, Point(round(dx+100+j*10-80*cos(angle)),
                    round(dy+100-90*sin(angle))),
                    Point(round(dx+100+j*10-30*cos(angle)),
                    round(dy+100-30*sin(angle))), white, 1, 8, 0)

        ellipse( img, Point(dx+150, dy+100), Size(100,70), 0, 0, 360, white, -1, 8, 0 )
        ellipse( img, Point(dx+115, dy+70), Size(30,20), 0, 0, 360, black, -1, 8, 0 )
        ellipse( img, Point(dx+185, dy+70), Size(30,20), 0, 0, 360, black, -1, 8, 0 )
        ellipse( img, Point(dx+115, dy+70), Size(15,15), 0, 0, 360, white, -1, 8, 0 )
        ellipse( img, Point(dx+185, dy+70), Size(15,15), 0, 0, 360, white, -1, 8, 0 )
        ellipse( img, Point(dx+115, dy+70), Size(5,5), 0, 0, 360, black, -1, 8, 0 )
        ellipse( img, Point(dx+185, dy+70), Size(5,5), 0, 0, 360, black, -1, 8, 0 )
        ellipse( img, Point(dx+150, dy+100), Size(10,5), 0, 0, 360, black, -1, 8, 0 )
        ellipse( img, Point(dx+150, dy+150), Size(40,10), 0, 0, 360, black, -1, 8, 0 )
        ellipse( img, Point(dx+27, dy+100), Size(20,35), 0, 0, 360, white, -1, 8, 0 )
        ellipse( img, Point(dx+273, dy+100), Size(20,35), 0, 0, 360, white, -1, 8, 0 )
        
    return img

if __name__=='__main__':
    img = generate_image()
        
    namedWindow( "image", 1 )
    imshow( "image", img )

    contours, hierarchy = findContours( img, RETR_TREE, CHAIN_APPROX_SIMPLE, Point(0,0) )

    # comment this out if you do not want approximation
    contours = vector_vector_Point2i([approxPolyDP_int(asMat(x), 3, 1) for x in contours])

    namedWindow( "contours", 1 )
    createTrackbar( "levels+3", "contours", levels, 7, on_trackbar )

    on_trackbar(0, None)
    waitKey(0)
