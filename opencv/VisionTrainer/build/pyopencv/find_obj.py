#!/usr/bin/env python
# OpenCV 2.x's C demo
# -- adapted further by Attila, Aug 2010
# -- adapted by Daniel to work with PyOpenCV
# -- modified a bit Minh-Tri Pham

import sys
import pyopencv as cv

# flann-based search
def findPairs(surf, objectKeypoints, objectDescriptors, imageKeypoints, imageDescriptors):
    ptpairs = []

    N = len(objectKeypoints)
    K = 2 # K as in K nearest neighbors
    dim = surf.descriptorSize()

    m_object = cv.asMat(objectDescriptors).reshape(1, N)
    m_image = cv.asMat(imageDescriptors).reshape(1, len(imageKeypoints))

    flann = cv.Index(m_image,cv.KDTreeIndexParams(4))

    indices = cv.Mat(N, K, cv.CV_32S)
    dists = cv.Mat(N, K, cv.CV_32F)

    flann.knnSearch(m_object, indices, dists, K, cv.SearchParams(250))
    
    indices = indices[:,0].ravel()
    dists = dists.ndarray
    
    for i in xrange(N):
        if dists[i,0] < 0.6*dists[i,1]:
            ptpairs.append((objectKeypoints[i].pt, imageKeypoints[int(indices[i])].pt))
    
    return ptpairs


# a rough implementation for planar object location
def locatePlanarObject(ptpairs, src_corners, dst_corners):
    import numpy as _n

    n = len(ptpairs)
    if n < 4:
        return 0
    pt1 = cv.asMat(_n.array([cv.asndarray(pair[0]) for pair in ptpairs]))
    pt2 = cv.asMat(_n.array([cv.asndarray(pair[1]) for pair in ptpairs]))
    h = cv.findHomography(pt1, pt2, method=cv.RANSAC, ransacReprojThreshold=5)[:]

    for i in range(4):
        x = src_corners[i].x
        y = src_corners[i].y
        Z = 1./(h[2,0]*x + h[2,1]*y + h[2,2])
        X = (h[0,0]*x + h[0,1]*y + h[0,2])*Z
        Y = (h[1,0]*x + h[1,1]*y + h[1,2])*Z
        dst_corners[i] = cv.Point(int(X), int(Y))

    return 1

if __name__ == '__main__':
    if len(sys.argv) == 3:
        object_filename = sys.argv[1]
        scene_filename = sys.argv[2]
    else:
        object_filename = "box.png"
        scene_filename = "box_in_scene.png"

    cv.namedWindow("Object", 1)
    cv.namedWindow("Object Correspond", 1)

    colors = [
        cv.Scalar(0,0,255),
        cv.Scalar(0,128,255),
        cv.Scalar(0,255,255),
        cv.Scalar(0,255,0),
        cv.Scalar(255,128,0),
        cv.Scalar(255,255,0),
        cv.Scalar(255,0,0),
        cv.Scalar(255,0,255),
        cv.Scalar(255,255,255),
    ]

    # read the two images
    object_color = cv.imread( object_filename, cv.CV_LOAD_IMAGE_COLOR )
    image = cv.imread( scene_filename, cv.CV_LOAD_IMAGE_GRAYSCALE )
    if not object_color or not image:
        print("Can not load %s and/or %s\n" \
            "Usage: find_obj [<object_filename> <scene_filename>]\n" \
            % (object_filename, scene_filename))
        exit(-1)
    object = cv.Mat(object_color.size(), cv.CV_8UC1)
    cv.cvtColor( object_color, object, cv.CV_BGR2GRAY )
    
    # corners
    src_corners = [cv.Point(0,0), cv.Point(object.cols, 0), cv.Point(object.cols, object.rows), cv.Point(0, object.rows)]
    dst_corners = [cv.Point()]*4

    # find keypoints on both images
    surf = cv.SURF(500, 4, 2, True)
    mask = cv.Mat()
    tt = float(cv.getTickCount())    
    objectKeypoints = cv.vector_KeyPoint()
    objectDescriptors = surf(object, mask, objectKeypoints)
    print("Object Descriptors: %d\n" % len(objectKeypoints))
    imageKeypoints = cv.vector_KeyPoint()
    imageDescriptors = surf(image, mask, imageKeypoints)
    print("Image Descriptors: %d\n" % len(imageKeypoints))
    tt = float(cv.getTickCount()) - tt
    print("Extraction time = %gms\n" % (tt/(cv.getTickFrequency()*1000.)))
    
    # create a correspond Mat
    correspond = cv.Mat(image.rows+object.rows, image.cols, cv.CV_8UC1, cv.Scalar(0))
    
    # copy the images to correspond -- numpy way
    correspond[:object.rows, :object.cols] = object[:]
    correspond[object.rows:, :image.cols] = image[:]

    # find pairs
    ptpairs = findPairs(surf, objectKeypoints, objectDescriptors, imageKeypoints, imageDescriptors)

    for pair in ptpairs:
        cv.line( correspond, cv.asPoint(pair[0]), cv.Point(int(pair[1].x), int(pair[1].y+object.rows)), colors[8] )

    # locate planar object
    if locatePlanarObject( ptpairs, src_corners, dst_corners ):
        for i in range(4):
            r1 = dst_corners[i]
            r2 = dst_corners[(i+1)%4]
            cv.line( correspond, cv.Point(r1.x, r1.y+object.rows ), cv.Point(r2.x, r2.y+object.rows ), colors[8] )

    # show the object correspondents
    cv.imshow("Object Correspond", correspond)
    
    # draw circles
    for keypt in objectKeypoints:
        cv.circle(object_color, cv.asPoint(keypt.pt), int(keypt.size*1.2/9.*2), colors[0], 1, 8, 0)
    cv.imshow("Object", object_color)
        
    cv.waitKey(0)
    
