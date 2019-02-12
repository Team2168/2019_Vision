import numpy as np
import cv2
import FalconEyeMap
import time

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture('../target_samples/field_panel_2_rocket.avi')

while(1):
    # Slows video to 10 fps
    time.sleep(0.1)

    _, frame = cap.read()

    # Converts frame to grayscale, then to a binary image
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayscale, FalconEyeMap.LOWER_BRIGHTNESS, FalconEyeMap.UPPER_BRIGHTNESS, 0)

    # Finds the contours within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filters out contours with small areas
    i = 0
    contoursLen = len(contours)
    while i < contoursLen:
        currContour = contours[i]
        if cv2.contourArea(currContour) < FalconEyeMap.CONTOUR_SIZE_THRESHOLD:
            del contours[i]
            i-=1
            contoursLen-=1
        i+=1

    if len(contours) >= 2:
        lowestError = None
        bestContour = None
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            aspectRatio = rect[1][0] / rect[1][1]
            angle = rect[2]

            # Finds the percent error for aspect ratio and angle
            rightAspectRatioError = abs((aspectRatio - FalconEyeMap.TARGET_ASPECT_RATIO_RIGHT) / FalconEyeMap.TARGET_ASPECT_RATIO_RIGHT)
            leftAspectRatioError = abs((aspectRatio - FalconEyeMap.TARGET_ASPECT_RATIO_LEFT) / FalconEyeMap.TARGET_ASPECT_RATIO_LEFT)
            if rightAspectRatioError <= leftAspectRatioError:
                aspectRatioError = rightAspectRatioError
            else:
                aspectRatioError = leftAspectRatioError
            rightAngleError = abs((angle - FalconEyeMap.TARGET_ANGLE_DEGREES_RIGHT) / FalconEyeMap.TARGET_ANGLE_DEGREES_RIGHT)
            leftAngleError = abs((angle - FalconEyeMap.TARGET_ANGLE_DEGREES_LEFT) / FalconEyeMap.TARGET_ANGLE_DEGREES_LEFT)
            if rightAngleError <= leftAngleError:
                angleError = rightAngleError
            else:
                angleError = leftAngleError

            error = aspectRatioError + angleError

            # If there is no lowest error, then this contour has the lowest error and is the new best target
            if lowestError == None or error <= lowestError:
                lowestError = error
                bestContour = contour

        # Draws a rectangle around the best target
        bestRect = cv2.minAreaRect(bestContour)
        bestBox = cv2.boxPoints(bestRect)
        bestBox = np.int0(bestBox)
        cv2.drawContours(frame, [bestBox], 0, (0,0,255), 2)

    # Displays frame and thresh
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    # Closes the program if Esc is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()