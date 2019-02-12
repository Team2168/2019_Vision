""" @file: falconthreads.py
    @class: FalconThreads
    @description:
    
"""
import threading
import cv2

from imagedata import ImageData 
from imageprocessor import ImageProcessor
from imageprocessing import BasicAlgorithm
from imageprocessing import AdvancedAlgorithm

import FalconEyeMap

""" @class: FalconThreads
    @description:
    
"""
class FalconThreads(threading.Thread):
    def setSharedData(self, sharedData):
            self.sharedData = sharedData
    def endThread(self):
        self.keepRunning = False
    def run(self):
        raise NotImplementedError

""" List all threads that will be used
    in the FalconEye application
"""
class TCPDataOut(FalconThreads):
    def run(self):
        pass

class TCPDataIn(FalconThreads):
    def run(self):
        pass

class MJPEGServer(FalconThreads):
    def run(self):
        pass

class DebugVideoFeed(FalconThreads):
    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            time.sleep(1/30)
            print("show...")
            cv2.imshow("Frame", self.sharedData.frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()

class RetrieveImage(FalconThreads):
    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            time.sleep(1/60)
            self.sharedData.getFrame()

class ProcessImage(FalconThreads):
    def run(self):
        self.keepRunning = True

        """ Image Processor is the context for the image processing
            algorithms we are developing. We can plug and play with
            any of the implemented algorithms by dorpping them into
            the Image Processor constructor or using the setAlgorithm
            method.
        """
        self.imgProcessor = ImageProcessor(BasicAlgorithm(self.sharedData))
        while self.keepRunning:
            self.imgProcessor.processImage()

class MainThread(FalconThreads):
    """ Setup all threads
    """
    def setupThreads(self):
        # Shared data to connect all image services
        self.imData = ImageData(FalconEyeMap.VID_3)

        # Retireve image thread
        self.recvImg = RetrieveImage()
        self.recvImg.setSharedData(self.imData)

        # Processing image thread
        self.imgProcess = ProcessImage()
        self.imgProcess.setSharedData(self.imData)

        # Show the video window (Debbugging only)
        self.debugFeed = DebugVideoFeed()
        self.debugFeed.setSharedData(self.imData)

    """ Start all threads
    """
    def startThreads(self):
        self.recvImg.start()
        self.imgProcess.start()

        self.debugFeed.start()

    """ Kill all threads when main ends
    """
    def endThread(self):
        self.keepRunning = False

        self.recvImg.endThread()
        self.recvImg.join()

        self.imgProcess.endThread()
        self.imgProcess.join()

        self.debugFeed.endThread()
        self.debugFeed.join()

    def run(self):
        """ Setup all threads
        """
        self.setupThreads()

        """ Start all threads
        """
        self.startThreads()

        self.keepRunning = True
        while self.keepRunning:
            time.sleep(1)

        """ End all threads
        """
        self.endThread()
        


if __name__=='__main__':
    import time
    main = MainThread()
    main.start()
    time.sleep(10)
    main.endThread()
    main.join()
