from typing import List, Tuple, Union
import cv2
import numpy as np
from . import utils

def resample_array(in_arr: np.ndarray, out_shape: Union[Tuple, List]=None, in_pix: Union[float, int]=None, out_pix: Union[float, int]=None, interpolation: str='linear') -> np.ndarray:
    """
    Method that resamples arrays using the shape or the pixel size.

    :param in_arr: 2D/3D Image array
    :param out_shape: Tuple of output array dimension (e.g. (nrows, ncols))
    :param in_pix: Input pixel size. Provide instead of out_shape. For non-square
    pixels, provide a tuple (psy, psx)
    :param out_pix: Output pixel size. Provide along with in_pix instead of out_shape.
    For non-square pixels, provide a tuple (psy, psx)
    :param interpolation: Interpolation method. Choose between linear, cubic, lanczos.
    :return: Resampled array, Adjusted Geo-transformation
    """
    inter_method = {'linear': cv2.INTER_LINEAR, 'cubic': cv2.INTER_CUBIC, 'lanczos': cv2.INTER_LANCZOS4}
    try:
        assert utils.find_dtype(in_arr) in ('uint8', 'uint16', 'float32')
    except AssertionError:
        in_arr = in_arr.astype(utils.find_dtype(in_arr)[1])
    if out_shape:
        if not in_arr.shape == out_shape:
            resampled = cv2.resize(in_arr, out_shape, interpolation=inter_method[interpolation])
        else:
            resampled = in_arr
    elif in_pix and out_pix:
        if not isinstance(in_pix, (list, tuple)) and (not isinstance(out_pix, (list, tuple))):
            scalr = in_pix / out_pix
            resampled = cv2.resize(in_arr, None, fx=scalr, fy=scalr, interpolation=inter_method[interpolation])
        else:
            scalrx = in_pix[1] / out_pix[1]
            scalry = in_pix[0] / out_pix[0]
            resampled = cv2.resize(in_arr, None, fx=scalrx, fy=scalry, interpolation=inter_method[interpolation])
    else:
        resampled = None
    return resampled

def convert8bit(nbit_image: np.ndarray) -> np.ndarray:
    """
    Method to convert any n-Bit image to 8-bit with contrast enhancement
    (histogram truncation).

    :param nbit_image: 2D or 3D array
    :return: 8-bit image
    """

    def _make_8bit(arr: np.ndarray) -> np.ndarray:
        av_val = np.mean(arr)
        std_val = np.std(arr)
        min_val = av_val - 1.96 * std_val
        min_val = min_val if min_val >= 0 else 0
        max_val = av_val + 1.96 * std_val
        arr[arr > max_val] = max_val
        arr[arr < min_val] = min_val
        arr = np.divide(arr - min_val, max_val - min_val) * 255
        return arr
    bit8_img = np.dstack(nbit_image).astype(np.float32)
    nbit_image = None
    if bit8_img.ndim == 3:
        for i in range(bit8_img.shape[2]):
            bit8_img[..., i] = _make_8bit(bit8_img[..., i])
    else:
        bit8_img = _make_8bit(bit8_img)
    return bit8_img

def multiband2grayscale(img: np.ndarray) -> np.ndarray:
    """
    Function to convert point coordinates to geojson format.

    :param img: Multichannel image array.
    :return: Grayscale image
    """
    try:
        assert img.ndim == 3
    except AssertionError:
        return img
    img_sum = np.sum(img, axis=2)
    img_weights_arr = np.dstack([np.divide(img[..., i], img_sum) for i in range(img.shape[2])])
    channel_weights = np.nanmean(img_weights_arr, axis=(0, 1))
    while channel_weights.sum() > 1.0:
        channel_weights -= channel_weights * 0.01
    gray = np.sum(img * channel_weights, axis=2)
    return gray

def get_sliding_win(in_arr: np.ndarray, ksize: int, step_x: int=1, step_y: int=1, pad: bool=True) -> np.ndarray:
    """
    Efficient method that returns sliced arrays for sliding windows.

    :param in_arr: 2D or 3D array
    :param ksize: Odd integer window size
    :param step_x: Step or stride size in the x-direction (def=1)
    :param step_y: Step or stride size in the y-direction (def=1)
    :param pad: Flag to enable image padding equal to the radius of ksize
    :return: 4D array matching the input array's size. Each element is an array
    matching the window size+bands
    """
    from numpy.lib.stride_tricks import as_strided
    if pad:
        ksize += 1 - ksize % 2
        radius = ksize // 2
        pad_widths = [[radius, radius], [radius, radius]]
        if in_arr.ndim == 3:
            pad_widths += [[0, 0]]
        in_arr = np.pad(in_arr, pad_widths, 'reflect')
    else:
        radius = 0
    if in_arr.ndim == 2:
        (sy, sx) = in_arr.shape
        nbands = False
    elif in_arr.ndim == 3:
        (sy, sx, nbands) = in_arr.shape
    else:
        raise ValueError(f'Incorrect array shape {in_arr.shape}')
    if not nbands:
        strides = (in_arr.strides[0] * step_y, in_arr.strides[1] * step_x) + in_arr.strides
        out_shape = ((sy - ksize + 2 * radius + step_y) // step_y, (sx - ksize + 2 * radius + step_x) // step_x, ksize, ksize)
    else:
        strides = (in_arr.strides[0] * step_y, in_arr.strides[1] * step_x, in_arr.strides[2]) + in_arr.strides
        out_shape = ((sy - ksize + 2 * radius + step_y) // step_y, (sx - ksize + 2 * radius + step_x) // step_x, 1, ksize, ksize, nbands)
    sliced_array = as_strided(in_arr, shape=out_shape, strides=strides)
    return sliced_array

def get_tiles(in_arr: np.ndarray, ksize: Union[int, List[int], Tuple[int]]=None, nblocks: int=None) -> np.ndarray:
    """
    Efficient method that returns sliced arrays for sliding windows.

    :param in_arr: 2D or 3D array
    :param ksize: Integer window size or List/Tuple of window sizes in x and y
    directions
    :param nblocks: Integer number of tiles in which to divide the array or
    List/Tuple of number ot tiles in x and y directions
    :return: 4D array matching the input array's size. Each element is an array
    matching the window size+bands
    """
    from numpy.lib.stride_tricks import as_strided
    if ksize:
        if isinstance(ksize, (list, tuple)):
            ksize_x = ksize[0]
            ksize_y = ksize[1]
            step_x = ksize[0]
            step_y = ksize[1]
        else:
            ksize_x = ksize
            ksize_y = ksize
            step_x = ksize
            step_y = ksize
    elif nblocks:
        if isinstance(nblocks, (list, tuple)):
            ksize_x = in_arr.shape[1] // nblocks[0]
            ksize_y = in_arr.shape[0] // nblocks[1]
            step_x = ksize_x
            step_y = ksize_y
        else:
            ksize_x = in_arr.shape[1] // nblocks
            ksize_y = in_arr.shape[0] // nblocks
            step_x = ksize_x
            step_y = ksize_y
    if in_arr.ndim == 2:
        (sy, sx) = in_arr.shape
        nbands = False
    elif in_arr.ndim == 3:
        (sy, sx, nbands) = in_arr.shape
    else:
        raise ValueError(f'Incorrect array shape {in_arr.shape}')
    if not nbands:
        strides = (in_arr.strides[0] * step_y, in_arr.strides[1] * step_x) + in_arr.strides
        out_shape = (sy // step_y, sx // step_x, ksize_y, ksize_x)
    else:
        strides = (in_arr.strides[0] * step_y, in_arr.strides[1] * step_x, in_arr.strides[2]) + in_arr.strides
        out_shape = (sy // step_y, sx // step_x, 1, ksize_y, ksize_x, nbands)
    sliced_array = as_strided(in_arr, shape=out_shape, strides=strides)
    return sliced_array