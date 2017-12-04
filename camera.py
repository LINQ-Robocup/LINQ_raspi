# coding:utf-8

import cv2.cv as cv
import time

cv.NamedWindow("camera", 1)

capture = cv.CaptureFromCAM(0)

# 画像サイズの指定
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,320)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,240)

while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera", img)
    if cv.WaitKey(10) > 0:
        break
cv.DestroyAllWindows()
