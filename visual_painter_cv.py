import cv2 as cv
import numpy as np
import mediapipe as mp
import time 
import os 
import handTrackers as htm

brushThick =15
erasser =35

xp,yp =0,0
folderpath = "header"
mylist = os.listdir(folderpath)
print(mylist)
canvas = np.zeros((720,1280,3),dtype='uint8')
overlay=[]
drawcolor =(255,0,0)
for img in mylist:
    image = cv.imread(f'{folderpath}/{img}')
    overlay.append(image)

header = overlay[0]

cap =cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = htm.handDetector(detectionCon=0.40)
while True:
    # 1. importing image
    success, image = cap.read()
    image = cv.flip(image,1)

      
    #2. find Landmarks
    image = detector.findHands(image)
    lmList = detector.findPosition(image,draw=False)

    if len(lmList) !=0:
        x1 , y1 = lmList[8][1:]
        x2 , y2 = lmList[12][1:]
        #3. checking fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        # 4 . checking selection mode -Two fingers up

        if fingers[1] and fingers[2] :
            xp, yp = 0, 0
            print("Selection Mode ")

            if y1 <125:
                if 50<x1 <327:
                    header = overlay[0]
                    drawcolor=(255,0,2)
                elif 328<x1 <584 :
                    header = overlay[1]
                    drawcolor = (255, 0, 255)
                elif 600  < x1 < 1049:
                    header = overlay[2]
                    drawcolor = (0, 255, 0)
                elif 1089 < x1 < 1270:
                    header = overlay[3]
                    drawcolor = (0, 0, 0)
            cv.rectangle(image, (x1, y1 - 25), (x2, y2 + 25), drawcolor, -1)
        # 5. checking drawing mode - single finger up
        
        if fingers[1] and fingers[2] == False:
            print("Drawing Mode ")
            cv.circle(image,(x1,y1),20,drawcolor,-1)
            if xp==0 and yp ==0:
                xp ,yp =x1,y1
            if drawcolor ==(0,0,0):
                cv.line(image, (xp, yp), (x1, y1), drawcolor, erasser)
                cv.line(canvas, (xp, yp), (x1, y1), drawcolor, erasser)
            cv.line(image,(xp,yp),(x1,y1),drawcolor,brushThick)
            cv.line(canvas, (xp, yp), (x1, y1), drawcolor, brushThick)
            xp,yp = x1,y1
    imageGray = cv.cvtColor(canvas,cv.COLOR_BGR2GRAY)

    thres, imagInv = cv.threshold(imageGray,20,255,cv.THRESH_BINARY_INV)
    imagInv = cv.cvtColor(imagInv,cv.COLOR_GRAY2BGR)
    image =cv.bitwise_and(image,imagInv)
    image = cv.bitwise_or(image,canvas)

    image[0:125,0:1280] =header
    cv.imshow('painter',image)
    # cv.imshow('canvas',canvas)
    if cv.waitKey(1) & 0xFF ==ord('q'):
        break