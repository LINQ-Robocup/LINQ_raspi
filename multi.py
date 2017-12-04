import cv2
import numpy as np
import sys
import os
import serial

# global variables
mbed = None
cap = None
cap2 = None

temp_h = None
temp_s = None
temp_u = None

def recognizeVictim(camera):
    # === variables ===

    victims = ""

    max_h = 0
    max_s = 0
    max_u = 0

    top_left_h = (0,0)
    bottom_right_h = (0,0)

    top_left_s = (0,0)
    bottom_right_s = (0,0)

    top_left_u = (0,0)
    bottom_right_u = (0,0)
    # ==================

    if camera == 0:
        ret, frame = cap.read()
    else:
        ret, frame = cap2.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thresh = 70
    max_pixel = 255
    ret, frame = cv2.threshold(frame, thresh, max_pixel, cv2.THRESH_BINARY)

    #detect H
    result = cv2.matchTemplate(frame, temp_h, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.40:	
        # global top_left_h
        top_left_h = max_loc
        w, h = temp_h.shape[::-1]
        # global bottom_right_h
        bottom_right_h = (top_left_h[0] + w, top_left_h[1] + h)	
        max_h = max_val
        
    #detect S
    result = cv2.matchTemplate(frame, temp_s, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.40:	
        # global top_left_s
        top_left_s = max_loc
        w, h = temp_h.shape[::-1]
        # global bottom_right_s
        bottom_right_s = (top_left_s[0] + w, top_left_s[1] + h)	
        max_s = max_val

        
    #detect U
    result = cv2.matchTemplate(frame, temp_u, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.40:	
        # global top_left_u
        top_left_u = max_loc
        w, h = temp_h.shape[::-1]
        # global bottom_right_u
        bottom_right_u = (top_left_u[0] + w, top_left_u[1] + h)	
        max_u = max_val
 
    result = max_h
    victims = "H"
    
    if result < max_s:
        result = max_s
        victims = "S"

    if result < max_u:
        result = max_u
        victims = "U"

    
    if victims == "H":
        cv2.rectangle(frame, top_left_h, bottom_right_h, (0, 0, 200), 5)
        cv2.putText(frame,"H", (top_left_h[0] -10, top_left_h[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
    if victims == "S":
        cv2.rectangle(frame, top_left_s, bottom_right_s, (0, 0, 200), 5)
        cv2.putText(frame,"S", (top_left_s[0] -10, top_left_s[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
   
    if victims == "U":
        cv2.rectangle(frame, top_left_u, bottom_right_u, (0, 0, 200), 5)
        cv2.putText(frame,"U", (top_left_u[0] -10, top_left_u[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
    
    # print "Camera: " + str(camera) + " | " + victims + " | " + str(max_h) + " | " + str(max_s) + " | " + str(max_u)
    
    if camera == 0:
        cv2.imshow('Camera0', frame)
    else:
        cv2.imshow('Camera1', frame)  

    return victims  			


def init():
    global cap, cap2, temp_h, temp_s, temp_u, mbed
    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        sys.exit()
    cap2 = cv2.VideoCapture(1)
    if cap2.isOpened() is False:
        sys.exit()
    cap.set(3, 320)
    cap.set(4, 240)
    cap2.set(3, 320)
    cap2.set(4, 240)
    temp_h = cv2.imread('maze_H.png', 0)
    temp_s = cv2.imread('maze_S.png', 0)
    temp_u = cv2.imread('maze_U.png', 0)
    #frame = cv2.imread('maze_H.png', 0)

    if os.system('ls -al /dev/ttyACM0') is 0:
        mbed = serial.Serial('/dev/ttyACM0')
    else:
        mbed = serial.Serial('/dev/ttyACM1')

# main
init()
while True:
    getdata = mbed.read(1)
    print getdata
    if getdata is 'r':
        camera0 = recognizeVictim(0)
        if camera0 is 'H':
            mbed.write("4");
            print "send 54"
        elif camera0 is 'S':
            mbed.write("5")
            print "send 55"
        elif camera0 is 'U':
            mbed.write("6")
            print "send 56"

    elif getdata is 'l':
        camera1 = recognizeVictim(1)
        if camera1 is 'H':
            mbed.write("7");
            print "send 57"
        elif camera1 is 'S':
            mbed.write("8")
            print "send 58"
        elif camera1 is 'U':
            mbed.write("9")
            print "send 59"
    

cap.release()
cap2.release()
cv2.destroyAllWindows()
