import unittest
from cameramodels.data import kinect_v2_camera_info
from cameramodels.data import kinect_v2_image
from cameramodels import PinholeCameraModel

class TestData(unittest.TestCase):

    def test_kinect_v2_image(self):
        kinect_v2_image()

    def test_kinect_v2_camera_info(self):
        info_path = kinect_v2_camera_info()
        PinholeCameraModel.from_yaml_file(info_path)