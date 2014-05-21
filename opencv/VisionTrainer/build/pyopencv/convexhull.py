#!/usr/bin/env python
# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv

print("OpenCV Python version of convexhull")

# import the necessary things for OpenCV
from pyopencv import *

# to generate random values
import random

# how many points we want at max
_MAX_POINTS = 100

if __name__ == '__main__':

    # main object to get random values from
    my_random = random.Random ()

    # create the image where we want to display results
    image = Mat(Size(500, 500), CV_8UC3)

    while True:
        # do forever

        # get a random number of points
        count = my_random.randrange (0, _MAX_POINTS) + 1

        # initialisations
        points = Mat(Size(count, 1), CV_32SC2)
        
        for i in range (count):
            # generate a random point
            points[0,i] = (my_random.randrange (0, image.cols / 2) + image.cols / 4,
                my_random.randrange (0, image.cols / 2) + image.cols / 4)

        # compute the convex hull
        hull = convexHull_int(points)
        points = asvector_Point2i(points)
        
        # start with an empty image
        image[:] = 0

        for i in range (count):
            # draw all the points
            circle (image, points[i], 2, Scalar (0, 0, 255), CV_FILLED, CV_AA, 0)

        # start the line from the last point
        pt0 = hull[-1]
        
        for pt1 in hull:
            # draw
            line (image, pt0, pt1, Scalar (0, 255, 0), 1, CV_AA, 0)

            # now, current one will be the previous one for the next iteration
            pt0 = pt1

        # display the final image
        imshow ('hull', image)

        # handle events, and wait a key pressed
        if waitKey (0) & 255 == 27:
            # user has press the ESC key, so exit
            break
