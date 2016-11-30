#!/usr/bin/env python2

'''Color extraction.'''

import argparse
import numpy as np
import cv2

# Construct the argument parser and parse arguments
# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--image', help='/path/to/image/file')
# args = vars(parser.parse_args())
# image = cv2.imread(args['image'])

image1 = cv2.imread('/home/akhan/Pictures/Webcam/2016-11-19-124734.jpg')
image1 = cv2.bilateralFilter(image1, 9, 75, 75)
image1 = cv2.fastNlMeansDenoisingColored(image1, None, 10, 10, 7, 21)
hsv_i1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
image2 = cv2.imread('/home/akhan/Pictures/Webcam/2016-11-19-124741.jpg')
image2 = cv2.bilateralFilter(image2, 9, 75, 75)
image2 = cv2.fastNlMeansDenoisingColored(image2, None, 10, 10, 7, 21)
hsv_i2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

# define list of boundaries
boundaries = [
	([81,90,60], [115,144,85]),        # Green
	([76,172,160], [121,199,205]),     # Yellow
	([190,170,134], [212,176,140]),    # White
	([63,92,149], [68,98,180]),        # Orange
	([62,56,88], [75,80,116]),         # Red
	([180,77,35], [186,131,75])        # Blue
]

# Loop over these boundaries
for (lower, upper) in boundaries:
	# Create NumPy arrays from the boundaries
	lower = np.array(lower, dtype='uint8')
	upper = np.array(upper, dtype='uint8')

	# Find the colors within the specified boundaries and apply the mask.
	mask = cv2.inRange(image2, lower, upper)
	output = cv2.bitwise_and(image2, image2, mask=mask)

	# Show the images
	cv2.imshow("Images", np.hstack([image2, output]))
	cv2.waitKey(0)

print 'Done.'
