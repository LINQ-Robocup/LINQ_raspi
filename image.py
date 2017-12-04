import cv2
import numpy as np

temp_h = cv2.imread('maze_H.png', 0)
temp_s = cv2.imread('maze_S.png', 0)
temp_u = cv2.imread('maze_U.png', 0)
frame = cv2.imread('devide.png', 0)

devide = 300/2;

blackLeft = 0
blackRight = 0

for i in range(300):
	for j in range(206):
    		
		if frame[j,i] == 0:
			if i < devide :
				blackLeft += 1
			else :
				blackRight += 1

			
print "Left:", blackLeft, "Right:",blackRight

# print temp,
while True:
	thresh = 70
	max_pixel = 255
	ret, frame = cv2.threshold(frame, thresh, max_pixel, cv2.THRESH_BINARY)


	cv2.imshow('capture', frame)
	k = cv2.waitKey(1)
	if k == 13:
		break

cv2.destroyAllWindows()
