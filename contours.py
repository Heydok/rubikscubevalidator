import argparse
import imutils
import cv2
import glob
import numpy as np

def auto_canny(image, sigma=0.33):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

wide = cv2.Canny(blurred, 10, 200)
tight = cv2.Canny(blurred, 255, 250)
auto = auto_canny(blurred)

cv2.imshow('image_window_1', image)

combined = cv2.addWeighted(wide, 0.7, tight, 0.3, 0)
combined = cv2.addWeighted(combined, 0.7, auto, 0.3, 0)
(thresh, im_binary) = cv2.threshold(combined, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow("Edges", im_binary)
#cv2.imshow("All images", np.hstack([wide, tight, auto]))
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
