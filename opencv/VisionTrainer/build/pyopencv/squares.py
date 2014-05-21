#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
#
# The full "Square Detector" program.
# It loads several images subsequentally and tries to find squares in
# each image
#

from pyopencv import *
from math import sqrt
import numpy as NP
import numpy.linalg as NL

thresh = 50
img = Mat()
img0 = Mat()
wndname = "Square Detection Demo"

def angle( pt1, pt2, pt0 ):
    d1 = pt1[:] - pt0[:]
    d2 = pt2[:] - pt0[:]
    return NP.dot(d1, d2)/(NL.norm(d1)*NL.norm(d2)+1e-5)

def findSquares4( img, thresh ):
    N = 11
    sz = Size( img.cols & -2, img.rows & -2 )
    timg = img.clone() # make a copy of input image
    gray = Mat(sz, CV_8UC1)
    pyr = Mat( Size(int(sz.width/2), int(sz.height/2)), CV_8UC3 )
    # create empty sequence that will contain points -
    # 4 points per square (the square's vertices)
    squares = vector_vector_Point2i()

    # select the maximum ROI in the image
    # with the width and height divisible by 2
    subimage = Mat(sz, img.type())

    # down-scale and upscale the image to filter out the noise
    pyrDown( timg, pyr, pyr.size() )
    pyrUp( pyr, subimage, subimage.size() )
    # extract the color planes
    tgrays = vector_Mat()
    channels = vector_Mat()
    split( timg, tgrays )
    split( subimage, channels ) 
    # find squares in every color plane of the image
    for c in range(3):
        for l in range(N):
            # hack: use Canny instead of zero threshold level.
            # Canny helps to catch squares with gradient shading
            if( l == 0 ):
                # apply Canny. Take the upper threshold from slider
                # and set the lower to 0 (which forces edges merging)
                Canny( tgrays[c], gray, 0, thresh, 5 )
                # dilate canny output to remove potential
                # holes between edge segments
                dilate( gray, gray, Mat() )
            else:
                # apply threshold if l!=0:
                #     tgray(x,y) = gray(x,y) < (l+1)*255/N ? 255 : 0
                threshold( tgrays[c], gray, (l+1)*255/N, 255, THRESH_BINARY )

            # find contours and store them all as a list
            contours, hierarchy = findContours(gray, mode=RETR_LIST, method=CHAIN_APPROX_SIMPLE)

            if len(contours) == 0:
                continue
            
            # test each contour
            for contour in contours:
                # approximate contour with accuracy proportional
                # to the contour perimeter
                contour = asMat(contour)
                result = approxPolyDP_int( contour, arcLength(contour, False)*0.02, False )
                # square contours should have 4 vertices after approximation
                # relatively large area (to filter out noisy contours)
                # and be convex.
                # Note: absolute value of an area is used because
                # area may be positive or negative - in accordance with the
                # contour orientation
                if len(result) != 4:
                    continue
                res_mat = asMat(result)
                if abs(contourArea(res_mat)) > 1000 and isContourConvex(res_mat):
                    s = 0;
                    for i in range(4):
                        # find minimum angle between joint
                        # edges (maximum of cosine)
                        t = abs(angle( res_mat[0,i], res_mat[0,i-2], res_mat[0,i-1]))
                        if s<t:
                            s=t
                    # if cosines of all angles are small
                    # (all angles are ~90 degree) then write quandrange
                    # vertices to resultant sequence
                    if( s < 0.3 ):
                        squares.append(result)

    return squares

def on_trackbar( a, param ):
    if not img.empty():
        squares = findSquares4( img, a )
        cpy = img.clone()        
        # draw the squares as a closed polylines
        polylines( cpy, squares, 1, CV_RGB(0,255,0), 3, CV_AA, 0 );
        # show the resultant image
        imshow( wndname, cpy );

names =  ["pic1.png", "pic2.png", "pic3.png", "pic4.png", "pic5.png", "pic6.png" ];

if __name__ == "__main__":
    for name in names:
        img0 = imread( name, 1 )
        if img0.empty():
            print("Couldn't load %s" % name)
            continue
        img = img0.clone()
        # create window and a trackbar (slider) with parent "image" and set callback
        # (the slider regulates upper threshold, passed to Canny edge detector)
        namedWindow( wndname, 1 )
        createTrackbar( "canny thresh", wndname, thresh, 1000, on_trackbar )
        # force the image processing
        on_trackbar(0, None)
        # wait for key.
        # Also the function cvWaitKey takes care of event processing
        c = waitKey(0)
        if( c & 255 == 27 ):
            break
