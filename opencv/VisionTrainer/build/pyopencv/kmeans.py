#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with pyopencv
from pyopencv import *
import numpy.random as NR
MAX_CLUSTERS=5

if __name__ == "__main__":

    color_tab = [CV_RGB(255,0,0),CV_RGB(0,255,0),CV_RGB(100,100,255), CV_RGB(255,0,255),CV_RGB(255,255,0)]
    img = Mat(Size(500, 500), CV_8UC3)
    rng = RNG()
    namedWindow( "clusters", 1 )
        
    while True:
        cluster_count = rng.as_uint()%(MAX_CLUSTERS-1) + 2
        
        # generate random sample from multigaussian distribution
        points = NR.randn(cluster_count, rng.as_uint()%200 + 1, 2)*(img.cols, img.rows)*0.1
        for k in range(cluster_count):
            points[k] += (rng.as_uint()%img.cols, rng.as_uint()%img.rows)
        sample_count = points.size/2
        points = asMat(points.reshape(sample_count, 1, 2).astype('float32'))
        randShuffle( points )
        
        # K Means Clustering
        clusters = Mat(points.size(), CV_32SC1)
        compact, centers = kmeans(points, cluster_count, clusters, 
            TermCriteria(TermCriteria.EPS+TermCriteria.MAX_ITER, 10, 1.0), 3, KMEANS_RANDOM_CENTERS)

        img.setTo(0)
        pts = points[:].reshape(sample_count, 2).astype('i')
        for i in range(sample_count):
            circle(img, asPoint(pts[i]), 2, color_tab[clusters[i,0]], CV_FILLED, CV_AA, 0)
        
        imshow( "clusters", img )

        if '%c' % (waitKey(0) & 255) in ['\x1b','q','Q']: # 'ESC'
            break
