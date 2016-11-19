#!/usr/bin/env python2

from shapedetector import ShapeDetector
from colorlabeler import ColorLabeler
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='/path/to/img')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

blurred = cv2.GaussianBlur(resized, (5,5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if imutils.is_cv2() else contours[1]

# Initialize shape and color detectors

sd = ShapeDetector()
cl = ColorLabeler()

for c in contours:
    M = cv2.moments(c)
    cX = int((M['m10'] / (M['m00'] + 1e-7)
