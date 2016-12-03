import numpy as np
import cv2

def auto_canny(image, sigma=0.33):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged


cap = cv2.VideoCapture(0)#Video cap object takes in the device # as a param
#I'm assuming we both have only one camera on our laptops, so 0 is fine.

if cap.isOpened():

	while(True):
		#Capture frame-by-frame
		ret, frame = cap.read()

		#Our operations on the frame come here
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (3, 3), 0)

		wide = cv2.Canny(blurred, 10, 200)
		tight = cv2.Canny(blurred, 255, 250)
		auto = auto_canny(blurred)

		combined = cv2.addWeighted(wide, 0.7, tight, 0.3, 0)
		combined = cv2.addWeighted(combined, 0.7, auto, 0.3, 0)
		(thresh, im_binary) = cv2.threshold(combined, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		cv2.imshow("Edges", im_binary)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	#When everything done, release the Capture
	cap.release()
	cv2.destroyAllWindows()
else:
	print "ERROR! Videocapture didn't open for some godless reason"