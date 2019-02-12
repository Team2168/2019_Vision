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
    def processImage(self):
        raise NotImplementedError

""" @class: BasicAlgorithm
    @description:
    Algorithm described here
"""
class BasicAlgorithm (ImageProcessingStrategy):
    def processImage(self):
        print("Basic Algotithm")

""" @class: AdvanceAlgorithm
    @description:
    Algorithm described here
"""
class AdvancedAlgorithm (ImageProcessingStrategy):
    def processImage(self):
        print("Advanced Algorithm")

