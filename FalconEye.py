import cv2
import numpy
import FalconEyeMap

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture(FalconEyeMap.TEST_CAM_1)

while(1):
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Sets the threshold for what brightness objects of interest must be
    _, thresh = cv2.threshold(gray, 200, 255, 0)
    # Finds the contours of everything within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    # If there are any contours, finds the center of each
    if(len(contours) > 0):
        for i in contours:
            if(cv2.contourArea(i) > 0):
                M = cv2.moments(i)
                cX = int(M['m10'] / M["m00"])
                cY = int(M["m01"] / M["m00"])

    # Draws a dot in the center of the contour
    cv2.circle(frame, (cX,cY), 5, (0,0,255), -1)

    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()