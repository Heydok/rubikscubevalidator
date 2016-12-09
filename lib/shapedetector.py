#!/usr/bin/env python2

'''
Taken from pyimagesearch
http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
'''

import cv2

class ShapeDetector:
    def __init__(self):
        pass


    def detect(self, contour):
        # Initialize the shape name and approximate the contour.
        shape = 'n/a'
        perimeter = cv2.arcLength(contour, True)
        # Ramer-Douglas-Peucker algorithm, "Split and Merge"
        approximation = cv2.approxPolyDP(contour,
            0.04 * perimeter, True)
        
        if len(approximation) == 3:
            shape = 'Triangle'

        elif len(approximation) == 4:
            '''Compute the bounding box of the contour and use the
            bounding box to compute the aspect ratio.'''
            (x, y, w, h) = cv2.boundingRect(approximation)
            aspect_ratio = w / float(h)

            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                shape = "Square"
            else:
                shape = "Rectangle"

        elif len(approximation) == 5:
            shape = "Pentagon"

        else:
            shape = "Circle"

        return shape


