""" @file: imageprocessing.py
    @class: ImageProcessingAlgorithm
    @description:
    Strategy pattern to quickly develop,
    apply and even implement multiple image processing
    algorithims on the fly
"""

import cv2
import FalconEyeMap

class ImageProcessingAlgorithm(object):
    def __init__(self, imageData):
        self.imgData = imageData
    def processImage(self):
        raise NotImplementedError

""" @class: BasicAlgorithm
    @description:
    Algorithm described here
"""
class BasicAlgorithm (ImageProcessingAlgorithm):
    def calculateError(self, experimental, ideal):
        return abs((experimental - ideal)/ideal)

    def isLeft(self, aspectLeft, angleLeft):
        aspectInTolerance = aspectLeft <= FalconEyeMap.TARGET_ASPECT_RATIO_PERCENTAGE
        angleInTolerance = angleLeft <= FalconEyeMap.TARGET_ANGLE_PERCENTAGE
        return (aspectInTolerance and angleInTolerance)

    def isRight(self,aspectRight, angleRight):
        aspectInTolerance = aspectRight <= FalconEyeMap.TARGET_ASPECT_RATIO_PERCENTAGE
        angleInTolerance = angleRight <= FalconEyeMap.TARGET_ANGLE_PERCENTAGE
        return (aspectInTolerance and angleInTolerance)

    def processImage(self):
        self.imgData.contours, _ = cv2.findContours(self.imgData.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        #Ensure at least 2 contours present
        if len(self.imgData.contours)>=2:
            i=0
            while i < len(self.imgData.contours):
                if cv2.contourArea(self.imgData.contours[i]) < FalconEyeMap.CONTOUR_SIZE_THRESHOLD:
                    del self.imgData.contours[i]
                    i-=1
                i+=1
            #Ensure largest contours get processed first
            self.imgData.contours = sorted(self.imgData.contours, key=lambda x: cv2.contourArea(x), reverse=True)
            if i>7:
                self.imgData.contours = self.imgData.contours[0:7]

            """ Get data on each contour
            """
            for candidate in self.imgData.contours:
                rect = cv2.minAreaRect(candidate)
                cx = rect[0][0]
                cy = rect[0][1]
                contourWidth = rect[1][0]
                contourHeight = rect[1][1]
                angle = rect[2]
                aspectRatio = contourWidth/contourHeight

                """ Calculate error for each contour (at most 8 contours)
                    % Error = |exp - ideal| * 100
                              -------------
                                  ideal
                
                    Calculate error for:
                        1. Aspect Ration = W/H
                        2. Angle, proximity to 14.5 degrees
                        3. Fingerprint as:
                            a) left strip
                            b) right strip
                            c) neither
                """

                aspectErrorLeft = self.calculateError(aspectRatio, FalconEyeMap.TARGET_ASPECT_RATIO_LEFT)
                aspectErrorRight = self.calculateError(aspectRatio, FalconEyeMap.TARGET_ASPECT_RATIO_RIGHT)

                angleErrorLeft = self.calculateError(angle, FalconEyeMap.TARGET_ANGLE_DEGREES_LEFT)
                angleErrorRight = self.calculateError(angle, FalconEyeMap.TARGET_ANGLE_DEGREES_RIGHT)

                if self.isLeft(aspectErrorLeft, angleErrorLeft):
                    print("left")
                elif self.isRight(aspectErrorRight, angleErrorRight):
                    print("right")
                else:
                    print("neither")

""" @class: AdvanceAlgorithm
    @description:
    Algorithm described here
"""
class AdvancedAlgorithm (ImageProcessingAlgorithm):
    def processImage(self):
        print("Advanced Algorithm")

