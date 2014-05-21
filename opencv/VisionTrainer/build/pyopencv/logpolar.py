#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
import sys
from pyopencv import *

src=None
dst=None
src2=None

def on_mouse( event, x, y, flags, param ):

    if( not src ):
        return;

    if event==CV_EVENT_LBUTTONDOWN:
        logPolar( src, dst, Point2f(x,y), 40, INTER_LINEAR+CV_WARP_FILL_OUTLIERS )
        logPolar( dst, src2, Point2f(x,y), 40, INTER_LINEAR+CV_WARP_FILL_OUTLIERS+CV_WARP_INVERSE_MAP )
        imshow( "log-polar", dst )
        imshow( "inverse log-polar", src2 )

if __name__ == "__main__":
    
    filename = "fruits.jpg"
    if len(sys.argv)>1:
        filename=argv[1]
    
    src = imread(filename, CV_LOAD_IMAGE_COLOR)
    if not src:
        print("Could not open %s" % filename)
        sys.exit(-1)
        
    namedWindow( "original",1 )
    namedWindow( "log-polar", 1 )
    namedWindow( "inverse log-polar", 1 )
  
    
    dst = Mat(Size(256,256), CV_8UC3 )
    src2 = Mat(src.size(), CV_8UC3 )
    
    setMouseCallback( "original", on_mouse )
    on_mouse( CV_EVENT_LBUTTONDOWN, src.cols/2, src.rows/2, None, None)
    
    imshow( "original", src )
    waitKey()
