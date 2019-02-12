import numpy as np
import cv2
import FalconEyeMap
import time

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture('../target_samples/field_panel_2_rocket.avi')

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

        if len(sortedContours) >= 8:
            largestContours = list()
            for i in range(8):
                largestContours[i] = sortedContours[i]
        else:
            largestContours = sortedContours

        for contour in largestContours:
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

    # Displays the frame and thresh
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    # Closes the program if Esc is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()