import numpy as np
import cv2

cap = cv2.VideoCapture(0)#Video cap object takes in the device # as a param
#I'm assuming we both have only one camera on our laptops, so 0 is fine.

if cap.isOpened():

	while(True):
		#Capture frame-by-frame
		ret, frame = cap.read()

		#Our operations on the frame come here
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		'''
		The above essentially captures, frame by frame, in grayscale,
		an image from video.
		We pretty much have to do our work within one iteration of this frame.
		Any work is to be done on the current frame, received from gray.
		All our work will be done within one loop of while, until ord() gets q.
		'''
		#Display the resulting frame (Simplest example of using the data from the current fram)
		cv2.imshow('frame', gray)#In this case, all we do is display it.

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	#When everything done, release the Capture
	cap.release()
	cv2.destroyAllWindows()
else:
	print "ERROR! Videocapture didn't open for some godless reason"