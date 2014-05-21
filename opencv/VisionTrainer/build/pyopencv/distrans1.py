#!/usr/bin/env python

# Old-style OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
import sys
from pyopencv import *

wndname = "Distance transform"
tbarname = "Threshold"

# The output images
dist = None
dist8u1 = None
dist8u2 = None
dist8u = None
dist32s = None

gray = None
edge = None

# define a trackbar callback
def on_trackbar( edge_thresh, param ):

    threshold( gray, edge, edge_thresh, edge_thresh, THRESH_BINARY )
    #Distance transform                  
    distanceTransform( edge, dist, CV_DIST_L2, CV_DIST_MASK_5 )

    dist.convertTo(dist, dist.type(), 5000.0, 0 )
    pow( dist, 0.5, dist )
    
    dist.convertTo( dist32s, dist32s.type(), 1.0, 0.5 )
    bitwise_and( dist32s, Scalar.all(255), dist32s )
    dist32s.convertTo( dist8u1, dist8u1.type(), 1, 0 )
    dist32s.convertTo( dist32s, dist32s.type(), -1, 0 )
    bitwise_and( dist32s, Scalar.all(255), dist32s )
    dist32s.convertTo( dist8u2, dist8u2.type(), 1, 0 )
    merge( vector_Mat.fromlist([dist8u1, dist8u2, dist8u2]), dist8u )
    imshow( wndname, dist8u )


if __name__ == "__main__":
    edge_thresh = 100

    filename = "stuff.jpg"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    gray = imread( filename, 0 )
    if gray.empty():
        print("Failed to load %s" % filename)
        sys.exit(-1)

    # Create the output image
    dist = Mat(gray.size(), CV_32FC1 )
    dist8u1 = gray.clone()
    dist8u2 = gray.clone()
    dist8u = Mat(gray.size(), CV_8UC3 )
    dist32s = Mat(gray.size(), CV_32SC1 )

    # Convert to grayscale
    edge = gray.clone()
    
    # create the window
    namedWindow( wndname, CV_WINDOW_AUTOSIZE )

    # create a toolbar 
    createTrackbar( tbarname, wndname, edge_thresh, 255, on_trackbar )

    # Show the image
    on_trackbar(edge_thresh, None)

    # Wait for a key stroke; the same function arranges events processing
    waitKey(0)
