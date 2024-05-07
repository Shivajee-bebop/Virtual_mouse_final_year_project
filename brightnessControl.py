import cv2
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc
import numpy as np
import HandTrackingModule as htm
import time

pTime = 0
b_level = 100

detector = htm.handDetector()

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

while True:

	success, img = cap.read()
	img = detector.findHands(img)
	landmarkList = detector.findPosition(img)

	# If landmarks list is not empty
	if landmarkList != []:
		# store x,y coordinates of (tip of) thumb
		x_1, y_1 = landmarkList[4][1:]

		# store x,y coordinates of (tip of) middle finger
		x_2, y_2 = landmarkList[12][1:]

		# draw circle on thumb and middle finger tip
		cv2.circle(img, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
		cv2.circle(img, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)

		# draw line from tip of thumb to tip of index finger
		cv2.line(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)

		# calculate square root of the sum of
		# squares of the specified arguments.
		L = hypot(x_2-x_1, y_2-y_1)

		# 1-D linear interpolant to a function
		# with given discrete data points
		# (Hand range 15 - 220, Brightness
		# range 0 - 100), evaluated at length.
		b_level = np.interp(L, [50, 150], [0, 100])

		# set brightness
		sbc.set_brightness(int(b_level))

	# Display Video and when 'q' is entered, destroy
	# the window
	cTime = time.time()
	fps = 1 / (cTime - pTime)
	pTime = cTime
	cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)
	if b_level:
		cv2.putText(img, f'Brightness: {int(b_level)}', (10, 100), cv2.FONT_HERSHEY_COMPLEX,
					1, (255, 0, 0), 3)
	cv2.imshow('Image', img)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break
