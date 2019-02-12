""" @file: imageprocessing.py
    @class: ImageProcessingAlgorithm
    @description:
    Strategy pattern to quickly develop,
    apply and even implement multiple image processing
    algorithims on the fly
"""
class ImageProcessingAlgorithm(object):
    def __init__(self):
        pass
    def processImage(self, imageData):
        raise NotImplementedError

""" @class: BasicAlgorithm
    @description:
    Algorithm described here
"""
class BasicAlgorithm (ImageProcessingAlgorithm):
    def processImage(self, imageData):
        print("Basic Algotithm")

""" @class: AdvanceAlgorithm
    @description:
    Algorithm described here
"""
class AdvancedAlgorithm (ImageProcessingAlgorithm):
    def processImage(self, imageData):
        print("Advanced Algorithm")

