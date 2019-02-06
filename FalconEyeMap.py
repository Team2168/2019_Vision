TEST_CAM_1 = 0
TEST_CAM_2 = 1
FRONT_CAM_IP = "http://10.21.68.90/mjpg/video.mjpg"
BACK_CAM_IP = "http://10.21.68.91/mjpg/video.mjpg"

LOWER_BRIGHTNESS = 250
UPPER_BRIGHTNESS = 255

CONTOUR_SIZE_THRESHOLD = 165.0 #Varies by camera

""" Target Specs for 2019 Deep Space
"""
TARGET_WIDTH = 2.0
TARGET_LENGTH = 5.5
TARGET_ANGLE_DEGREES_RIGHT = -14.5
TARGET_ANGLE_DEGREES_LEFT = -75.5
TARGET_ANGLE_PERCENTAGE = 0.25
TARGET_ASPECT_RATIO_RIGHT = TARGET_WIDTH/TARGET_LENGTH
TARGET_ASPECT_RATIO_LEFT = TARGET_WIDTH/TARGET_LENGTH
TARGET_ASPECT_RATIO_PERCENTAGE = 0.25