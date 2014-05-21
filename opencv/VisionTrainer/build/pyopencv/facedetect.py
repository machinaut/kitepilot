#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
import sys
from pyopencv import *

cascadeName = "minhtri_frontalface.xml"
nestedCascadeName = "haarcascade_eye_tree_eyeglasses.xml"

def detectAndDraw(img, cascade, nestedCascade, scale):
    i = 0
    t = 0.0
    colors =  ( CV_RGB(0,0,255),
        CV_RGB(0,128,255),
        CV_RGB(0,255,255),
        CV_RGB(0,255,0),
        CV_RGB(255,128,0),
        CV_RGB(255,255,0),
        CV_RGB(255,0,0),
        CV_RGB(255,0,255))
    gray = Mat()
    smallImg = Mat( Size(round(img.cols/scale), round(img.rows/scale)), CV_8UC1 )

    cvtColor( img, gray, CV_BGR2GRAY )
    resize( gray, smallImg, smallImg.size(), 0, 0, INTER_LINEAR )
    equalizeHist( smallImg, smallImg )

    t = getTickCount()
    faces = cascade.detectMultiScale( smallImg, 
        1.1, 2, 0
        #|CascadeClassifier.FIND_BIGGEST_OBJECT
        #|CascadeClassifier.DO_ROUGH_SEARCH
        |CascadeClassifier.SCALE_IMAGE
        ,
        Size(30, 30) )
    t = getTickCount() - t
    print( "detection time = %lf ms\n" % (t/(getTickFrequency()*1000.)) )
    for i in range(len(faces)):
        r = faces[i]
        color = colors[i%8]
        center = Point(round((r.x + r.width*0.5)*scale), round((r.y + r.height*0.5)*scale))
        radius = round((r.width + r.height)*0.25*scale)
        circle( img, center, radius, color, 3, 8, 0 )
        if nestedCascade.empty():
            continue
        smallImgROI = smallImg(r)
        nestedObjects = nestedCascade.detectMultiScale( smallImgROI, 
            1.1, 2, 0
            #|CascadeClassifier.FIND_BIGGEST_OBJECT
            #|CascadeClassifier.DO_ROUGH_SEARCH
            #|CascadeClassifier.DO_CANNY_PRUNING
            |CascadeClassifier.SCALE_IMAGE
            ,
            Size(30, 30) )
        for nr in nestedObjects:
            center = Point(round((r.x + nr.x + nr.width*0.5)*scale), round((r.y + nr.y + nr.height*0.5)*scale))
            radius = round((nr.width + nr.height)*0.25*scale)
            circle( img, center, radius, color, 3, 8, 0 )
    imshow( "result", img )

if __name__ == '__main__':
    capture = VideoCapture()
    frame = Mat()
    image = Mat()
    scaleOpt = "--scale="
    cascadeOpt = "--cascade="
    nestedCascadeOpt = "--nested-cascade"
    nestedCascadeOptLen = len(nestedCascadeOpt)
    inputName = ""

    cascade = CascadeClassifier()
    nestedCascade = CascadeClassifier()
    scale = 1.0

    for i in range(len(sys.argv)):
        if sys.argv[i].startswith(cascadeOpt):
            cascadeName = sys.argv[i][len(cascadeOpt):]
        elif sys.argv[i].startswith(nestedCascadeOpt):
            if sys.argv[i][nestedCascadeOptLen] == '=':
                nestedCascadeName = sys.argv[i][nestedCascadeOptLen+1:]
            if not nestedCascade.load( nestedCascadeName ):
                print("WARNING: Could not load classifier cascade for nested objects")
        elif sys.argv[i].startswith(scaleOpt):
            try:
                scale = float(sys.argv[i][len(scaleOpt):])
                if scale < 1:
                    raise ValueError()
            except:
                scale = 1.0
        elif sys.argv[i][0] == '-':
            print("WARNING: Unknown option %s" % sys.argv[i])
        else:
            inputName = sys.argv[i]

    if not cascade.load( cascadeName ):
        print("ERROR: Could not load classifier cascade")
        print("Usage: facedetect [--cascade=\"<cascade_path>\"]\n" \
            "   [--nested-cascade[=\"nested_cascade_path\"]]\n" \
            "   [--scale[=<image scale>\n" \
            "   [filename|camera_index]\n")
        sys.exit(-1)

    if not inputName or inputName.isdigit():
        capture.open( int(inputName) )
    elif inputName:
        image = imread( inputName, 1 )
        if image.empty():
            capture.open( inputName )
    else:
        image = imread( "lena.jpg", 1 )

    namedWindow( "result", 1 )

    if capture.isOpened():
        while True:
            capture >> frame
            if frame.empty():
                break

            detectAndDraw( frame, cascade, nestedCascade, scale )

            if waitKey( 10 ) >= 0:
                break
    else:
        if not image.empty():
            detectAndDraw( image, cascade, nestedCascade, scale )
            waitKey(0)
        elif inputName:
            # assume it is a text file containing the
            # list of the image filenames to be processed - one per line
            try:
                f = open( inputName, "rt" )
                for buf in f.readlines():
                    buf = buf.rstrip()
                    print("file %s" % buf)
                    image = imread( buf, 1 )
                    if not image.empty():
                        detectAndDraw( image, cascade, nestedCascade, scale )
                        if '%c' % (waitKey(0) & 255) in ['\x1b','q','Q']: # 'ESC'
                            break;
            except IOError:
                pass
