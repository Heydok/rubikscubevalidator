import numpy as np
import cv2
import imutils
from lib.shapedetector import ShapeDetector
from lib.colorlabeler import ColorLabeler

def auto_canny(image, sigma=0.33):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged


cap = cv2.VideoCapture(0)  # Video cap object takes in the device # as a param
# I'm assuming we both have only one camera on our laptops, so 0 is fine.

if cap.isOpened():

	sd = ShapeDetector()
	cl = ColorLabeler()

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		resized = imutils.resize(frame, width=250)
		ratio = frame.shape[0] / float(resized.shape[0])

		# Our operations on the frame come here
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (3, 3), 0)
		lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)

		im_binary = cv2.Canny(resized, 20, 100)

		(thresh, im_binary) = cv2.threshold(im_binary, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


		if cv2.waitKey(1) & 0xFF == ord('c'):
				screen_cap = True

				cnts = cv2.findContours(im_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cnts = cnts[0] if imutils.is_cv2() else cnts[1]
				for c in cnts:
					# Detect the shape.
					shape = sd.detect(c)
					if shape == 'Square':  # We only care about squares.
						x,y,w,h = cv2.boundingRect(c)
						im_b_cpy = resized[y:y+h,x:x+w]
						print("FOUND A SQUARE!!!!!!!!!!!!!!!!!!!")
						cv2.drawContours(resized, [c], -1, (0,255,0), 1)
						boundingRect = cv2.boundingRect(c)
				while(screen_cap):
					cv2.imshow("Contour", resized)
					cv2.imshow("Square", im_b_cpy)
					if cv2.waitKey(1) & 0xFF == ord('x'):
						screen_cap = False
						cv2.destroyWindow("Contour")

		else:
			cv2.imshow("Live Feed", im_binary)

					
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the Capture
	cap.release()
	cv2.destroyAllWindows()
else:
	print "ERROR! Videocapture didn't open for some godless reason"
