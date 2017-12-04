import cv2
import numpy as np
from time import sleep
import sys

#cap = cv2.CaptureFromCAM(0)
cap = cv2.VideoCapture(0)
count = 0
if cap.isOpened() is False:
	print "Open Failed Recconecting..."
	sys.exit()
# print cap.isOpened
cap.set(3, 320)
cap.set(4, 240)
temp_h = cv2.imread('maze_H.png', 0)
temp_s = cv2.imread('maze_S.png', 0)
temp_u = cv2.imread('maze_U.png', 0)
#frame = cv2.imread('maze_H.png', 0)

while True:
	victims = ""
	max_u = 0
	max_s = 0
	max_h = 0
	ret, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	thresh = 70
	max_pixel = 255
	ret, frame = cv2.threshold(frame, thresh, max_pixel, cv2.THRESH_BINARY)

	#detect H
	result = cv2.matchTemplate(frame, temp_h, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	if max_val > 0.40:	
		top_left = max_loc
		w, h = temp_h.shape[::-1]
		bottom_right = (top_left[0] + w, top_left[1] + h)	
		cv2.rectangle(frame, top_left, bottom_right, (0, 0, 200), 5)
		cv2.putText(frame,"H", (top_left[0] -10, top_left[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
		max_h = max_val
		
	#detect S
	result = cv2.matchTemplate(frame, temp_s, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	if max_val > 0.40:	
		top_left = max_loc
		w, h = temp_h.shape[::-1]
		bottom_right = (top_left[0] + w, top_left[1] + h)	
		cv2.rectangle(frame, top_left, bottom_right, (0, 0, 200), 5)
		cv2.putText(frame,"S", (top_left[0] -10, top_left[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
		max_s = max_val

		
	#detect U
	result = cv2.matchTemplate(frame, temp_u, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	if max_val > 0.40:	
		top_left = max_loc
		w, h = temp_h.shape[::-1]
		bottom_right = (top_left[0] + w, top_left[1] + h)	
		cv2.rectangle(frame, top_left, bottom_right, (0, 0, 200), 5)
		cv2.putText(frame,"U", (top_left[0] -10, top_left[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
		max_u = max_val
 
	result = max_h
	victims = "H"
	
	if result < max_s:
			result = max_s
			victims = "S"

	if result < max_u:
			result = max_u
			victims = "U"

	# print victims + "\t" + str(max_h) + "\t" + str(max_s) + "\t" + str(max_u)
	print top_left
	cv2.imshow('capture', frame)
	k = cv2.waitKey(1)
	if k == 13:
		break

cap.release()
cv2.destroyAllWindows()
