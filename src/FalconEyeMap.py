TEST_CAM_1 = 0
TEST_CAM_2 = 1
FRONT_CAM_IP = "http://10.21.68.90/mjpg/video.mjpg"
BACK_CAM_IP = "http://10.21.68.91/mjpg/video.mjpg"

LOWER_BRIGHTNESS = 15
UPPER_BRIGHTNESS = 50

CONTOUR_SIZE_THRESHOLD = 75.0 #Varies by camera 165.0
CONTOUR_MAX_SIZE = 1500.00

""" Target Specs for 2019 Deep Space
"""
TARGET_WIDTH = 2.0
TARGET_LENGTH = 5.5

TARGET_ANGLE_DEGREES_RIGHT = -14.5
TARGET_ANGLE_DEGREES_LEFT = -75.5
TARGET_ANGLE_PERCENTAGE = 0.25

TARGET_ASPECT_RATIO_RIGHT = TARGET_WIDTH/TARGET_LENGTH #0.3636
TARGET_ASPECT_RATIO_LEFT = TARGET_LENGTH/TARGET_WIDTH #2.75

TARGET_ASPECT_RATIO_PERCENTAGE = 0.25

""" Thread frequencies
"""
CAMERA_FPS = 30
GET_IMG_FREQ = 1/4*CAMERA_FPS

SHOW_IMAGE_FREQ = GET_IMG_FREQ*2

#For testing and debugging
VID_1 = "../target_samples/field.avi"
VID_2 = "../target_samples/field_static.avi"
VID_3 = "../target_samples/field_panel_2_rocket.avi"