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
        lowestError = None
        secondLowestError = None
        bestTarget = None
        secondBestTarget = None
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
            if lowestError == None:
                lowestError = error
                bestTarget = contour
            # Otherwise, if there is no second-lowest error, find one
            elif secondLowestError == None:
                # If contour has the new lowest error, contour is the new best target and the previous best is now the second-best
                if error < lowestError:
                    secondLowestError = lowestError
                    secondBestTarget = bestTarget
                    lowestError = error
                    bestTarget = contour
                # If contour doesn't have the new lowest error, it has the second-lowest and is the new second-best contour
                else:
                    secondLowestError = error
                    secondBestTarget = contour
            # Otherwise, if this contour's error is lower than lowestError, it is the new best target
            elif error <= lowestError:
                secondLowestError = lowestError
                secondBestTarget = bestTarget
                lowestError = error
                bestTarget = contour
            # Otherwise, if this contour's error is lower than secondBestError, it is the new second-best target
            elif error <= secondLowestError:
                secondLowestError = error
                secondBestTarget = contour

        # Draws a rectangle around the best target
        bestRect = cv2.minAreaRect(bestTarget)
        bestBox = cv2.boxPoints(bestRect)
        bestBox = np.int0(bestBox)
        cv2.drawContours(frame, [bestBox], 0, (0,0,255), 2)

        # Draws a rectangle around the second-best target
        secondBestRect = cv2.minAreaRect(secondBestTarget)
        secondBestBox = cv2.boxPoints(secondBestRect)
        secondBestBox = np.int0(secondBestBox)
        cv2.drawContours(frame, [secondBestBox], 0, (0,0,255), 2)

    # Displays frame and thresh
    cv2.imshow("frame", frame)
    cv2.imshow("thresh", thresh)

    # Closes the program if Esc is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()