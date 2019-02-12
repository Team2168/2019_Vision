import numpy as np
import cv2
import FalconEyeMap
import time

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture('../target_samples/field_static.avi')

distance = None

while(1):
    # Slows video to 10 fps
    time.sleep(0.1)

    _, frame = cap.read()

    # Converts frame to grayscale, then to a binary image
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayscale, FalconEyeMap.LOWER_BRIGHTNESS, FalconEyeMap.UPPER_BRIGHTNESS, 0)

    # Finds the contours within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) >= 2:
        # Sorts contours from largest to smallest
        sortedContours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        # Stores and draws largest target
        largestTarget = sortedContours[0]
        largestRect = cv2.minAreaRect(largestTarget)
        largestBox = cv2.boxPoints(largestRect)
        largestBox = np.int0(largestBox)
        cv2.drawContours(frame, [largestBox], 0, (0,255,0), 2)

        # Stores center and dimensions of largest target
        largestRectCX = largestRect[0][0]
        largestRectCY = largestRect[0][1]
        largestRectHeight = largestRect[1][0]
        largestRectWidth = largestRect[1][1]

    # Displays frame and thresh
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    # Closes the program if Esc is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()