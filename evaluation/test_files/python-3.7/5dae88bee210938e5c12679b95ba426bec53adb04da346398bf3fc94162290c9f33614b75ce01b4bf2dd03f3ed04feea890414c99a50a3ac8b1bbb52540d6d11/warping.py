"""Affine-warping and cropping an image."""
from mt import np
import mt.geo2d as g2
from . import cv2 as cv
__all__ = ['do_warp_image', 'warp_image', 'crop_image']

def do_warp_image(out_image: np.ndarray, in_image: np.ndarray, inv_tfm: g2.Aff2d, inter_mode: str='nearest', border_mode: str='constant'):
    """Takes an inverse warping transformation which goes from output image to input image and warps the input image.

    Parameters
    ----------
    out_image : numpy.ndarray
        output image to be warped and resized to
    in_image : numpy.ndarray
        input image from which the warping takes place
    inv_tfm : mt.geo.affine2d.Aff2d
        2D transformation mapping pixel locations in the output image to pixel locations in the
        input image
    inter_mode : {'nearest', 'bilinear'}
        interpolation mode. 'nearest' means nearest neighbour. 'bilinear' means bilinear
        interpolation
    border_mode : {'constant', 'replicate'}
        border filling mode. 'constant' means filling zero constant. 'replicate' means replicating
        last pixels in each dimension.
    """
    borderMode = cv.BORDER_CONSTANT if border_mode == 'constant' else cv.BORDER_REPLICATE
    interMode = cv.INTER_NEAREST if inter_mode == 'nearest' else cv.INTER_LINEAR
    cv.warpAffine(in_image, inv_tfm.matrix[:2, :], dst=out_image, dsize=(out_image.shape[1], out_image.shape[0]), flags=cv.WARP_INVERSE_MAP | interMode, borderMode=borderMode)

def warp_image(out_image: np.ndarray, in_image: np.ndarray, warp_tfm: g2.Aff2d, inter_mode: str='nearest', border_mode: str='constant'):
    """Takes a warping transformation mapping input image coordinates to the unit square, scales it to the output resolution, then warps the input image.

    Parameters
    ----------
    out_image : numpy.ndarray
        output image to be warped and resized to
    in_image : numpy.ndarray
        input image from which the warping takes place
    warp_tfm : mt.geo.affine2d.Aff2d
        2D transformation mapping pixel locations in the input image to the `[0,1]^2` square
    inter_mode : {'nearest', 'bilinear'}
        interpolation mode. 'nearest' means nearest neighbour. 'bilinear' means bilinear
        interpolation
    border_mode : {'constant', 'replicate'}
        border filling mode. 'constant' means filling zero constant. 'replicate' means replicating
        last pixels in each dimension.
    """
    inv_tfm = ~(g2.scale2d(out_image.shape[1], out_image.shape[0]) * warp_tfm)
    return do_warp_image(out_image, in_image, inv_tfm, inter_mode=inter_mode, border_mode=border_mode)

def crop_image(out_image: np.ndarray, in_image: np.ndarray, crop_rect: g2.Rect, inter_mode: str='nearest', border_mode: str='constant'):
    """Takes a crop window from input image and warp/resize it to output image.

    Parameters
    ----------
    out_image : numpy.ndarray
        output image to be cropped and resized to
    in_image : numpy.ndarray
        input image from which the crop takes place
    crop_rect : mt.geo.rect.Rect
        crop window
    inter_mode : {'nearest', 'bilinear'}
        interpolation mode. 'nearest' means nearest neighbour interpolation. 'bilinear' means
        bilinear interpolation
    border_mode : {'constant', 'replicate'}
        border filling mode. 'constant' means filling zero constant. 'replicate' means replicating
        last pixels in each dimension.
    """
    crop_tfm = g2.crop_rect(crop_rect)
    return warp_image(out_image, in_image, crop_tfm, inter_mode=inter_mode, border_mode=border_mode)