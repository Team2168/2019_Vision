import numpy as np
import cv2
import FalconEyeMap
import time

# Creates a capture from the specified camera or file
cap = cv2.VideoCapture('../target_samples/field_static.avi')
distance = 0
rect = None
roiRect = None
aspectRatio = None

def contourIsTarget(contour, side):
    if side == "left":
        targetAspectRatio = FalconEyeMap.TARGET_ASPECT_RATIO_LEFT
        targetAngleDegrees = FalconEyeMap.TARGET_ANGLE_DEGREES_LEFT
        tempRect = rect
    elif side == "right":
        targetAspectRatio = FalconEyeMap.TARGET_ASPECT_RATIO_RIGHT
        targetAngleDegrees = FalconEyeMap.TARGET_ANGLE_DEGREES_RIGHT
        tempRect = roiRect
    else:
        return False
    
    # Filters out contours with different aspect ratios than the vision target
    if aspectRatio > (targetAspectRatio - targetAspectRatio*FalconEyeMap.TARGET_ASPECT_RATIO_PERCENTAGE) and aspectRatio < (targetAspectRatio + targetAspectRatio*FalconEyeMap.TARGET_ASPECT_RATIO_PERCENTAGE):
        angle = tempRect[2]
        # Confirms contour is a left or right vision target
        if angle > (targetAngleDegrees + targetAngleDegrees*FalconEyeMap.TARGET_ANGLE_PERCENTAGE) and angle < (targetAngleDegrees - targetAngleDegrees*FalconEyeMap.TARGET_ANGLE_PERCENTAGE):
            return True
        else:
            return False
    else: return False


while 1:
    # Slows video to 10 fps
    time.sleep(0.1)

    _, frame = cap.read()
    
    # Converts frame to grayscale, then to a binary image
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayscale, FalconEyeMap.LOWER_BRIGHTNESS, FalconEyeMap.UPPER_BRIGHTNESS, 0)

    rows = thresh.shape[0]
    cols = thresh.shape[1]
   
    # Finds the contours of everything within the brightness threshold
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # First check: ensures there are at least two contours
    contoursLen = len(contours)
    i = 0

    if len(contours) >= 2:
        while i < contoursLen:
            currContour = contours[i]
            # Filters out contours with small areas
            if cv2.contourArea(currContour) < FalconEyeMap.CONTOUR_SIZE_THRESHOLD:
                del contours[i]
                i-=1
                contoursLen-=1
            i+=1
        # Sorts contours by area, from largest to smallest
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            aspectRatio = rect[1][0] / rect[1][1]
            if contourIsTarget(contour, "left"):
                cx = rect[0][0]
                cy = rect[0][1]
                contourWidth = rect[1][1]
                contourHeight = rect[1][0]

                # Creates a range of interest to the right of the contour
                rightmostCol = int(cx + 3*contourHeight)
                leftmostCol = int(cx - contourHeight)
                upperRow = int(cy + 2*contourHeight)
                lowerRow = int(cy - 2*contourHeight)

                # Ensures the range of interest fits within the frame
                if rightmostCol >= cols:
                    rightmostCol = cols
                if leftmostCol <= 0:
                    leftmostCol = 0
                if upperRow >= rows:
                    upperRow = rows
                if lowerRow <= 0:
                    lowerRow = 0

                roi = thresh[lowerRow:upperRow, leftmostCol:rightmostCol]
                subframe = frame[lowerRow:upperRow, leftmostCol:rightmostCol]
                cv2.imshow("Roi", roi)
                roiContours, hierarchy = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                roiContours = sorted(roiContours, key=lambda x: cv2.contourArea(x), reverse=True)
                if len(roiContours) >= 2:
                    for roiContour in roiContours:
                        roiRect = cv2.minAreaRect(roiContour)
                        aspectRatio = roiRect[1][0] / roiRect[1][1]
                        if contourIsTarget(roiContour, "right"):
                            cx2 = roiRect[0][0] + leftmostCol
                            cy2 = roiRect[0][1] + lowerRow
                            midpointX = int((cx + cx2)/2)
                            midpointY = int((cy + cy2)/2)
                            frameCenterX = int((0 + cols)/2)
                            frameCenterY = int((0 + rows)/2)
                            distance = abs(int(midpointX - frameCenterX))
                            cv2.line(frame, (midpointX, midpointY), (frameCenterX, frameCenterY), (0,0,255), 3)
                            break
            
                cv2.drawContours(subframe, roiContours, -1, (0,255,0), 3)
                frame[lowerRow:upperRow, leftmostCol:rightmostCol] = subframe
                break

    cv2.line(frame, (int((0 + cols)/2), 0), (int((0 + cols)/2), rows), (0,255,0), 3)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()