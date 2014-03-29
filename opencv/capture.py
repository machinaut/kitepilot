#!/usr/bin/env python
# capture.py - demo basic capture functionality

# need opencv installed. see http://opencv.org for more
import cv2

# Laptop webcam is '0', and our usb camera is probably '1'
# IF THIS DOESNT WORK TRY ANOTHER NUMBER :)
webcam = cv2.VideoCapture(1)
# VGA resolution
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)

rval, frame = webcam.read()
if not rval:
    print "ERROR CAPTURING FRAME"
    exit(1)

# Save the frame
cv2.imwrite('frame.jpg', frame)

# Display the frame
cv2.namedWindow('capture demo')
cv2.imshow('capture demo', frame)
print "Captured dimensions: ",frame.shape
print "Press a key (in the window) to exit."
cv2.waitKey(0) # wait for a keypress
cv2.destroyAllWindows() # nuke it all before exit
