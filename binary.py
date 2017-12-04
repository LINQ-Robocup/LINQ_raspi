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
	victims = ""
	ret, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	thresh = 70
	max_pixel = 25
	ret, frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)

	#detect H
	result = cv2.matchTemplate(frame, temp_h, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	top_left = max_loc
	w, h = temp_h.shape[::-1]
	bottom_right = (top_left[0] + w, top_left[1] + h)	
	cv2.rectangle(frame, top_left, bottom_right, (0, 0, 200), 10)
	cv2.putText(frame,"H", (top_left[0] -10, top_left[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)

        print str(max_val)
	cv2.imshow('capture', frame)
	k = cv2.waitKey(1)
	if k == 13:
		break

cap.release()
cv2.destroyAllWindows()
