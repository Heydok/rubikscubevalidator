#!/usr/bin/env python2

import numpy as np
import argparse
import cv2

# Construct the argument parser and parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', help='/path/to/image/file')
args = vars(parser.parse_args())

# Load image.
image = cv2.imread(args['image'])
# OpenCV stores images in BGR order instead of RGB

# Find all 'black' shapes in the image
lower = np.array([0,0,0])
upper = np.array([15,15,15])
shapeMask = cv2.inRange(image, lower, upper)

# Find the contours in the mask.
(contours, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

print 'Got {} black shapes.'.format(len(contours))
cv2.imshow('mask', shapeMask)
cv2.waitKey(0)

# Loop over the contours
for c in contours:
	# Draw and show the contour
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.imshow('image', image)
	cv2.waitKey(0)
