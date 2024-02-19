import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0 #previous time
cTime = 0 #current time
detector = htm.handDetector()
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lm = detector.findPosition(img)
    if len(lm) != 0:
        print(lm[4])

    ##CALCULATING FRAMERATE AND DISPLAY IT ON SCREEN

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)

    ##IMAGE DISPLAY
    cv2.imshow("Image", img)
    cv2.waitKey(1)