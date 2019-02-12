""" @file: imagedata.py
"""

import cv2

class ImageData(object):
    def __init__(self, cameraPort=0):
        self.camera = cv2.VideoCapture(cameraPort)
        self.frame = None
        self.thresh = None
    
    def __del__(self):
        self.camera.release()


    def getFrame(self):
        _, self.frame = self.camera.read()

if __name__ == '__main__':
    import time

    imData = ImageData(0)
    imData.getFrame()

    time.sleep(5)

    exit()

    