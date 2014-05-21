#!/usr/bin/env python
# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv

import sys

# import the necessary things for OpenCV
from pyopencv import *

#############################################################################
# so, here is the main part of the program

if __name__ == '__main__':

    # a small welcome
    print("OpenCV Python capture video")

    # first, create the necessary window
    namedWindow('Camera', CV_WINDOW_AUTOSIZE)

    # move the new window to a better place
    moveWindow('Camera', 10, 10)

    try:
        # try to get the device number from the command line
        device = int(sys.argv [1])

        # got it ! so remove it from the arguments
        del sys.argv [1]
    except (IndexError, ValueError):
        # no device number on the command line, assume we want the 1st device
        device = 0

    if len (sys.argv) == 1:
        # no argument on the command line, try to use the camera
        capture = VideoCapture(device)
    else:
        # we have an argument on the command line,
        # we can assume this is a file name, so open it
        capture = VideoCapture(sys.argv [1])            

    # check that capture device is OK
    if not capture.isOpened():
        print("Error opening capture device")
        sys.exit (1)

    # create a Mat instance
    frame = Mat()

    # capture the 1st frame to get some propertie on it
    capture >> frame

    # get size of the frame
    frame_size = frame.size()

    # get the frame rate of the capture device
    fps = capture.get(CV_CAP_PROP_FPS)
    if fps == 0:
        # no fps getted, so set it to 30 by default
        fps = 30

    # create the writer
    writer = VideoWriter ("captured.avi", CV_FOURCC('X','v','i','D'), fps, frame_size, True)

    # check the writer is OK
    if not writer.isOpened():
        print("Error opening writer")
        sys.exit (1)
        
    while True:
        # do forever

        # 1. capture the current image
        capture >> frame
        if frame.empty():
            # no image captured... end the processing
            break

        # write the frame to the output file
        writer << frame

        # display the frames to have a visual output
        imshow('Camera', frame)

        # handle events
        if waitKey (5) & 255 == 27:
            # user has press the ESC key, so exit
            break
