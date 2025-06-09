"""
    Postprocess module of crip.

    https://github.com/z0gSh1u/crip
"""
__all__ = ['drawCircle', 'fovCropRadius', 'fovCrop', 'muToHU', 'huToMu', 'huNoRescale', 'postlogsToProjections', 'binning']
import numpy as np
from .shared import *
from ._typing import *
from .utils import *

def drawCircle(slice: TwoD, radius: int, center=None) -> Tuple[NDArray, NDArray]:
    """
        Return points of a circle on `center` (slice center if `None`) with `radius`.

        This function can be used for preview FOV crop.
    """
    cripAssert(radius >= 1, 'radius should >= 1.')
    theta = np.arange(0, 2 * np.pi, 0.01)
    if center is None:
        center = (slice.shape[0] // 2, slice.shape[1] // 2)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return (x, y)

def fovCropRadius(SOD: float, SDD: float, detWidth: float, reconPixSize: float, roundOff=True) -> float:
    """
        Get the radius (in pixel) of the circle valid FOV of the reconstructed volume.

        Geometry:
            - SOD: Source Object Distance.
            - SDD: Source Detector Distance.
            - detWidth: Width of the detector, i.e., nElements * detElementWidth.
            - reconPixSize: Pixel size of the reconstructed image.
        
        Note that all these lengths should have same unit, like (mm) as recommended.
    """
    halfDW = detWidth / 2
    L = np.sqrt(halfDW ** 2 + SDD ** 2)
    Larc = SOD * np.arcsin(halfDW / L)
    r1 = Larc / reconPixSize
    Lflat = SOD / (SDD / detWidth) / 2
    r2 = Lflat / reconPixSize
    r3 = SOD / (L / halfDW) / reconPixSize
    r = min(r1, r2, r3)
    return round(r) if roundOff else r

@ConvertListNDArray
def fovCrop(img: TwoOrThreeD, radius: int, fill: Or[int, float]=0) -> ThreeD:
    """
        Crop a circle FOV on reconstructed image `img` with `radius` (pixel) \\
        and `fill` value for outside FOV.
    """
    cripAssert(radius >= 1 and isInt(radius), 'Invalid radius. Radius should be positive int.')
    cripAssert(is2or3D(img), 'img should be 2D or 3D.')
    (N, M) = img.shape[-2:]
    x = np.array(range(N), dtype=DefaultFloatDType) - N / 2 - 0.5
    y = np.array(range(M), dtype=DefaultFloatDType) - M / 2 - 0.5
    (xx, yy) = np.meshgrid(x, y)
    outside = xx ** 2 + yy ** 2 > radius ** 2
    cropped = img.copy()
    if is3D(img):
        cropped[:, outside] = fill
    else:
        cropped[outside] = fill
    return cropped

@ConvertListNDArray
def muToHU(image: TwoOrThreeD, muWater: float, b=1000) -> TwoOrThreeD:
    """
        Convert \\mu map to HU.
        
        `HU = (\\mu - \\muWater) / \\muWater * b`
    """
    cripAssert(is2or3D(image), '`image` should be 2D or 3D.')
    return (image - muWater) / muWater * b

@ConvertListNDArray
def huToMu(image: TwoOrThreeD, muWater: float, b=1000) -> TwoOrThreeD:
    """
        Convert HU to mu. (Invert of `MuToHU`.)
    """
    cripAssert(is2or3D(image), '`image` should be 2D or 3D.')
    return image / b * muWater + muWater

@ConvertListNDArray
def huNoRescale(image: TwoOrThreeD, b: float=-1000, k: float=1) -> TwoOrThreeD:
    """
        Invert the rescale-slope (y = kx + b) of HU value to get linear relationship between HU and mu.
    """
    cripAssert(is2or3D(image), '`image` should be 2D or 3D.')
    return (image - b) / k

def postlogsToProjections(postlogs: TwoOrThreeD, flat: Or[TwoD, float]) -> TwoOrThreeD:
    """
        Invert postlog images to the original projections.
    """
    res = np.exp(-postlogs) * flat
    return res