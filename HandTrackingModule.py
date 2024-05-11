import cv2
import mediapipe as mp
import time
import math



class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComp=1, detcectorConf=0.5, trackingConf=0.5):
        static_image_mode = mode
        max_num_hands = maxHands
        model_complexity = modelComp
        min_detection_confidence = detcectorConf
        min_tracking_confidence = trackingConf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode, max_num_hands, model_complexity,
                                        min_detection_confidence, min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # mediapipe accepts only rgb but opencv returns bgr
        self.results = self.hands.process(imgRGB)  # returns hand landmarks for multiple hands
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)  # draw connections for each hand between the landmarks
        return img
    def findPosition(self, img, handNo = 0, draw = False):
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape  # height,width and channels of the image
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), 3)
        return self.lmList
    def fingersUp(self, lm):
        fingerTipList=[4, 8, 12, 16, 20]  # tip for thumb,index,middle,ring and pinky
        fingersUpList=[]
        if len(lm) != 0:
            # for thumb
            if lm[fingerTipList[0]][1] < lm[fingerTipList[0]-1][1]:
                fingersUpList.append(1)
            else:
                fingersUpList.append(0)
            # for all other 4 fingers
            for i in range(1, 5):
                if lm[fingerTipList[i]][2] < lm[fingerTipList[i]-2][2]:
                    fingersUpList.append(1)
                else:
                    fingersUpList.append(0)
        return fingersUpList

    def findDistance(self, p1, p2, img, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length
        #return length, img, [x1, y1, x2, y2, cx, cy]





def main():
    pTime = 0 #previous time
    cTime = 0 #current time
    detector = handDetector()
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lm = detector.findPosition(img)
        if len(lm)!=0:
            print(lm[4])

        ##CALCULATING FRAMERATE AND DISPLAY IT ON SCREEN

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)

        ##IMAGE DISPLAY
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()