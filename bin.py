import cv2
import numpy as np

#cap = cv2.CaptureFromCAM(0)
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
temp_h = cv2.imread('maze_H.png', 0)
temp_s = cv2.imread('maze_S.png', 0)
temp_u = cv2.imread('maze_U.png', 0)
#frame = cv2.imread('maze_H.png', 0)

while True:
	ret, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	thresh = 70
        ret, frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)


	cv2.imshow('capture', frame)
	k = cv2.waitKey(1)
	if k == 13:
		break

cap.release()
cv2.destroyAllWindows()
