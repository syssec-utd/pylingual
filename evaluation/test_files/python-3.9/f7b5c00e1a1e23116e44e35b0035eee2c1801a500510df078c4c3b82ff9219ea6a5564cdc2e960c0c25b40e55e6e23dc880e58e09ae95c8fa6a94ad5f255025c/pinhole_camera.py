import copy
import logging
from typing import Union
from xrprimer_cpp.camera import PinholeCameraParameter as PinholeCameraParameter_cpp
from .camera import BaseCameraParameter

class PinholeCameraParameter(PinholeCameraParameter_cpp, BaseCameraParameter):
    ATTR_NAMES = BaseCameraParameter.ATTR_NAMES.copy()

    def __init__(self, K: Union[list, None]=None, R: Union[list, None]=None, T: Union[list, None]=None, name: str='default', height: int=1080, width: int=1920, world2cam: bool=True, convention: str='opencv', logger: Union[None, str, logging.Logger]=None) -> None:
        """A camera parameter class for pinhole camera model. This class has no
        distortion attributes and functions.

        Args:
            K (Union[list, np.ndarray, None], optional):
                Nested list of float32, 4x4 or 3x3 K mat.
                Defaults to None, 4x4 zeros.
            R (Union[list, np.ndarray, None], optional):
                Nested list of float32, 3x3 rotation mat.
                Defaults to None, 3x3 identity.
            T (Union[list, np.ndarray, None], optional):
                List of float32, T vector.
                Defaults to None, zero vector.
            name (str, optional):
                Name of this camera. Defaults to 'default'.
            height (int, optional):
                Height of the image shot by this camera.
                Defaults to 1080.
            width (int, optional):
                Width of the image shot by this camera.
                Defaults to 1920.
            world2cam (bool, optional):
                Whether the R, T transform points from world space
                to camera space. Defaults to True.
            convention (str, optional):
                Convention name of this camera.
                Defaults to 'opencv'.
            logger (Union[None, str, logging.Logger], optional):
                Logger for logging. If None, root logger will be selected.
                Defaults to None.
        """
        PinholeCameraParameter_cpp.__init__(self)
        BaseCameraParameter.__init__(self, K=K, R=R, T=T, name=name, height=height, width=width, world2cam=world2cam, convention=convention, logger=logger)

    def clone(self) -> 'PinholeCameraParameter':
        """Clone a new CameraParameter instance like self.

        Returns:
            PinholeCameraParameter
        """
        new_cam_param = self.__class__(K=copy.deepcopy(self.get_intrinsic(k_dim=4)), R=copy.deepcopy(self.extrinsic_r), T=copy.deepcopy(self.extrinsic_t), name=self.name, height=self.height, width=self.width, world2cam=self.world2cam, convention=self.convention, logger=self.logger)
        return new_cam_param

    def SaveFile(self, filename: str) -> bool:
        """Dump camera name and parameters to a json file.

        Args:
            filename (str):
                Path to the dumped json file.

        Returns:
            bool: True if save succeed.
        """
        return PinholeCameraParameter_cpp.SaveFile(self, filename)

    def LoadFile(self, filename: str) -> bool:
        """Load camera name and parameters from a dumped json file.

        Args:
            filename (str):
                Path to the dumped json file.

        Returns:
            bool: True if load succeed.
        """
        return PinholeCameraParameter_cpp.LoadFile(self, filename)