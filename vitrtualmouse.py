import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import pyautogui as pyg

#######
wCam, hCam = 640, 480  # webcam width and height
pTime = 0  # previous time
cTime = 0  # current time
frameR = 100  # frame reduction value
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7.5
#######

# pyg.FAILSAFE = False
detector = htm.handDetector(maxHands=1)
screenWidth, screenHeight = pyg.size()  # screen width and height
#  print(screenWidth, screenHeight)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # setting camera width
cap.set(4, hCam)  # setting camera height

while True:
    success, img = cap.read()
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # x,y coordinate of index finger
        x2, y2 = lmList[12][1:]  # x,y coordinate of middle finger
        #  print(x1, y1, x2, y2)

    # find which all fingers are up
    fingerUpList = detector.fingersUp(lmList)  # list containing finger information 1:up 0:down
    # print(fingerUpList)
    if len(fingerUpList) != 0:
        if fingerUpList[1] == 1 and fingerUpList[2] == 0:  # if index finger is up and middle finger is down then Mouse move mode

            # scale the mouse movement to the whole screen
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, screenWidth))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, screenHeight))

            #  normalize the coordinate values inorder to get a smooth mouse movement and not be shaky
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyg.moveTo(screenWidth- clocX, clocY)  # move mouse screenWidth-x3 is done to flip the cursor movement
            cv2.circle(img, (x1, y1), 15, (255,255,0), cv2.FILLED)  # draw a circle at index tip to easily identify it
            plocX, plocY = clocX, clocY  # set current x,y coordinates as previous

        if fingerUpList[1] == 1 and fingerUpList[2] == 1:  # if both index and middle finger are up the Clicking mode
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)  # change circle color to indicate click
            pyg.click()  # click mouse

    # CALCULATING FRAME RATE AND DISPLAY IT ON SCREEN

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)

    ##IMAGE DISPLAY
    cv2.imshow("Image", img)
    cv2.waitKey(1)
