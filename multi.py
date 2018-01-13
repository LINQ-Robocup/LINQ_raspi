import cv2
import numpy as np
import sys
import os
import serial

# === global variables ===
mbed = None
cam = None
cam2 = None

victimTemplate_H = None
victimTemplate_S = None
victimTemplate_U = None

def recognizeVictim(camera):
    # === variables ===

    victims = ""

    maxPercentage_H = 0
    maxPercentage_S = 0
    maxPercentage_U = 0

    positionTopLeft_H = (0,0)
    positionBottomRight_H = (0,0)

    positionTopLeft_S = (0,0)
    positionBottomRight_S = (0,0)

    positionTopLeft_U = (0,0)
    positionBottomRight_U = (0,0)

    # ==================
    # === read image from camera & convert to binary image ===
    if camera == 0:
        ret, frame = cam.read()
    else:
        ret, frame = cam2.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thresh = 70
    max_pixel = 255
    ret, frame = cv2.threshold(frame, thresh, max_pixel, cv2.THRESH_BINARY)

    # ==================
    # === detect victims ===

    #detect H
    result = cv2.matchTemplate(frame, victimTemplate_H, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0:	
        positionTopLeft_H = max_loc
        w, h = victimTemplate_H.shape[::-1]
        positionBottomRight_H = (positionTopLeft_H[0] + w, positionTopLeft_H[1] + h)	
        maxPercentage_H = max_val
        
    #detect S
    result = cv2.matchTemplate(frame, victimTemplate_S, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0:	
        positionTopLeft_S = max_loc
        w, h = victimTemplate_H.shape[::-1]
        positionBottomRight_S = (positionTopLeft_S[0] + w, positionTopLeft_S[1] + h)	
        maxPercentage_S = max_val

        
    #detect U
    result = cv2.matchTemplate(frame, victimTemplate_U, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0:	
        positionTopLeft_U = max_loc
        w, h = victimTemplate_H.shape[::-1]
        positionBottomRight_U = (positionTopLeft_U[0] + w, positionTopLeft_U[1] + h)	
        maxPercentage_U = max_val

    # ========================
    # === select highest matching rate victim ===

    resultPercentage = 0
    victim = "N"
    
    if resultPercentage < maxPercentage_H:
        resultPercentage = maxPercentage_H
        victim = "H"

    if resultPercentage < maxPercentage_S:
        resultPercentage = maxPercentage_S
        victim = "S"

    if resultPercentage < maxPercentage_U:
        resultPercentage = maxPercentage_U
        victim = "U"

    
    if victim == "H":
        cv2.rectangle(frame, positionTopLeft_H, positionBottomRight_H, (0, 0, 200), 5)
        cv2.putText(frame,"H", (positionTopLeft_H[0] -10, positionTopLeft_H[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
    if victim == "S":
        cv2.rectangle(frame, positionTopLeft_S, positionBottomRight_S, (0, 0, 200), 5)
        cv2.putText(frame,"S", (positionTopLeft_S[0] -10, positionTopLeft_S[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
   
    if victim == "U":
        cv2.rectangle(frame, positionTopLeft_U, positionBottomRight_U, (0, 0, 200), 5)
        cv2.putText(frame,"U", (positionTopLeft_U[0] -10, positionTopLeft_U[1] -10), cv2.FONT_HERSHEY_PLAIN,5.0,(0,0,200),8)
    
    return victim

    # ==================
    if camera == 0:
        cv2.imshow('Camera0', frame)
    else:
        cv2.imshow('Camera1', frame) 
    cv2.waitKey(1)


def init():
    global cam, cam2, victimTemplate_H, victimTemplate_S, victimTemplate_U, mbed
    cam = cv2.VideoCapture(0)
    if cam.isOpened() is False:
        sys.exit()
    cam2 = cv2.VideoCapture(1)
    if cam2.isOpened() is False:
        sys.exit()
    cam.set(3, 320)
    cam.set(4, 240)
    cam2.set(3, 320)
    cam2.set(4, 240)
    victimTemplate_H = cv2.imread('images/maze_H.png', 0)
    victimTemplate_S = cv2.imread('images/maze_S.png', 0)
    victimTemplate_U = cv2.imread('images/maze_U.png', 0)

    if os.system('ls -al /dev/ttyACM0') is 0:
        mbed = serial.Serial('/dev/ttyACM0')
    else:
        mbed = serial.Serial('/dev/ttyACM1')

# === main ===
init()
while True:
    os.system('echo 255 > /sys/class/leds/led0/brightness')
    print "waiting serial signal..."
    getdata = mbed.read(1)
    os.system('echo 0 > /sys/class/leds/led0/brightness')
    print getdata
    if getdata is 'r':
        camera0 = recognizeVictim(0)
        if camera0 is 'H':
            mbed.write("1");
            print "send H49"
        elif camera0 is 'S':
            mbed.write("2")
            print "send S50"
        elif camera0 is 'U':
            mbed.write("3")
            print "send U51"
        elif camera0 is 'N':
            mbed.write('0')
            print "send N48"

    elif getdata is 'l':
        camera1 = recognizeVictim(1)
        if camera1 is 'H':
            mbed.write("1");
            print "send H49"
        elif camera1 is 'S':
            mbed.write("2")
            print "send S50"
        elif camera1 is 'U':
            mbed.write("3")
            print "send U51"
        elif camera1 is 'N':
            mbed.write('0')
            print "send N48"

    

cam.release()
cam2.release()
cv2.destroyAllWindows()
