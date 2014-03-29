#!/usr/bin/env python
# video.py - demo basic video processing

# need opencv installed. see http://opencv.org for more
import cv2, datetime

# Laptop webcam is '0', and our usb camera is probably '1'
webcam = cv2.VideoCapture(1)

# get some basic info about the camera
#width  = webcam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
#height = webcam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
#print "Webcam width: ", width, " height: ", height
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)

start = datetime.datetime.now()

# loop a bunch then exit
for i in range(100):
    rval, frame = webcam.read()
    if not rval:
        print "Error reading image!"
        exit(1)

    # smooth original image using 3x3 gaussian kernel
    cv2.GaussianBlur(frame, (3,3), 0)

end = datetime.datetime.now()
diff = end - start
# I'm getting about 9.9 seconds for 100 frames on my macbook for full res
# And 3.3 seconds for VGA resolution (640, 480)
print "100 runs in", diff.seconds + diff.microseconds*1E-6, "seconds"
