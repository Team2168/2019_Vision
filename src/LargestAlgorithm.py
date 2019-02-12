import numpy as np
import cv2
import FalconEyeMap
import time

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture('../target_samples/field_static.avi')

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

        # Stores the two largest contours
        largestTarget = sortedContours[0]
        secondLargestTarget = sortedContours[1]

        # Draws the two largest targets
        largestRect = cv2.minAreaRect(largestTarget)
        largestBox = cv2.boxPoints(largestRect)
        largestBox = np.int0(largestBox)
        secondLargestRect = cv2.minAreaRect(secondLargestTarget)
        secondLargestBox = cv2.boxPoints(secondLargestRect)
        secondLargestBox = np.int0(secondLargestBox)
        cv2.drawContours(frame, [largestBox], 0, (0,0,255), 2)
        cv2.drawContours(frame, [secondLargestBox], 0, (0,0,255), 2)

    # Displays the frame and thresh
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    # Closes the program if Esc is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()