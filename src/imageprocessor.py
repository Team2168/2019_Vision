""" @file: imageprocessing.py
    @description:
    This file will provide the context for the
    algorithms found in imageprocessing.py
    
    This class will serve as the interface for the 
    image processing algorithms and will allow
    us to continue to develop and tweak algorithms during
    the season and even facilitate the capability of
    switching algorithms at runtime if new target criteria
    is needed to help our robot see game pieces or targets
    better.
"""
from imageprocessing import BasicAlgorithm
from imageprocessing import AdvancedAlgorithm

""" @class: ImageProcessor
    @description:
    Context for ImageProcessingStrategy
"""
class ImageProcessor(object):
    def __init__(self, processStrategy):
        self.algorithm = processStrategy
    def processImage(self):
        self.algorithm.processImage()


if __name__=='__main__':
    img = ImageProcessor(BasicAlgorithm())
    img.processImage()