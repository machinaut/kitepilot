#!/usr/bin/env python

import sys
try:
	print "Trying new OpenCV!!!"
	import cv2
except:
	print "Trying Old OpenCV!!!!"
	import opencv


def diffImg(t0, t1, t2):
	d1 = opencv.absdiff(t2, t1)
	d2 = opencv.absdiff(t1, t0)
	return opencv.bitwise_and(d1, d2)

if len(sys.argv) < 2:
	print "\n"
	print "This program requires the input file as the first arguement"
	print "Example:"
	print "    ", sys.argv[0], "~/Video.mov"
	sys.exit()

vid_file = sys.argv[1]

video = opencv.VideoCapture(vid_file)



