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
		resized = imutils.resize(frame, width=720)
		ratio = frame.shape[0] / float(resized.shape[0])

		# Our operations on the frame come here
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (3, 3), 0)
		lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
		lab = imutils.resize(lab, width=720)
		# (thresh, im_binary) = cv2.threshold(blurred, 50, 100, cv2.THRESH_BINARY_INV)
		(thresh, im_binary) = cv2.threshold(blurred, 100, 250, cv2.THRESH_BINARY)

		# edged = cv2.Canny(im_binary, 30, 200)
		edged = auto_canny(im_binary)


		cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		# Sort the list from largest contours to smallest, and check only the first 10
		# Ideally, there should only ever be 9, for each panel of a rubik face
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
		for c in cnts:
			# Detect the shape.
			shape = sd.detect(c)
			if shape == 'Square':  # We only care about squares.
				x,y,w,h = cv2.boundingRect(c)
				current_square = resized[y:y+h,x:x+w]
				cv2.drawContours(resized, [c], -1, (0,255,0), 3)
				bounding_box = cv2.boundingRect(c)

				# Color detection code
				M = cv2.moments(c)
				cX = int((M["m10"] / M["m00"]) * ratio)
				cY = int((M["m01"] / M["m00"]) * ratio)
				color = cl.label(lab, c)
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				text = "{} {}".format(color, shape)
				cv2.putText(resized, text, (cX, cY),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

				if cv2.waitKey(1) & 0xFF == ord('c'):
					screen_cap = True
					while(screen_cap):
						cv2.imshow("Square", current_square)
						if cv2.waitKey(1) & 0xFF == ord('x'):
							screen_cap = False
							cv2.destroyWindow("Contour")			
		cv2.imshow("Live Feed", resized)
		# cv2.imshow("Binary", im_binary)
		# cv2.imshow("Gray", gray)
		# cv2.imshow("L*a*b*", lab)
					
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the Capture
	cap.release()
	cv2.destroyAllWindows()
else:
	print "ERROR! Videocapture didn't open for some godless reason"
