import numpy as np
from PIL import Image
from skimage import data
import matplotlib.pyplot as plt

class ImageUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_gp_image(i_image_name=None, i_return_name: bool=False):
        """Return general-purpose images in skimage site"""
        'Reference: https://scikit-image.org/docs/stable/auto_examples/data/plot_general.html#sphx-glr-auto-examples-data-plot-general-py'
        list_images = ('astronaut', 'binary_blobs', 'brick', 'colorwheel', 'camera', 'cat', 'checkerboard', 'clock', 'coffee', 'coins', 'eagle', 'grass', 'gravel', 'horse', 'logo', 'page', 'text', 'rocket')
        assert isinstance(i_image_name, (str, int))
        if isinstance(i_image_name, str):
            assert i_image_name in list_images
        else:
            assert isinstance(i_image_name, int)
            index = i_image_name % len(list_images)
            i_image_name = list_images[index]
        image = getattr(data, i_image_name)()
        if i_return_name:
            return (image, i_image_name)
        else:
            return image

    @staticmethod
    def resize(i_image=None, i_tsize=(128, 128), i_min=None, i_max=None):
        """Resize an image to size of i_tsize"""
        assert isinstance(i_image, np.ndarray)
        assert isinstance(i_tsize, (list, tuple))
        assert len(i_tsize) == 2
        assert i_tsize[0] > 0
        assert i_tsize[1] > 0
        tsize = (i_tsize[1], i_tsize[0])
        'Using min-max scaling to make unit8 image'
        if i_image.dtype != np.uint8:
            if i_min is None:
                min_val = np.min(i_image)
            else:
                assert isinstance(i_min, (int, float))
                min_val = i_min
            if i_max is None:
                max_val = np.max(i_image)
            else:
                assert isinstance(i_max, (int, float))
                max_val = i_max
            assert min_val <= max_val
            image = (i_image - min_val) / (max_val - min_val + 1e-10)
            image = (image * 255.0).astype(np.uint8)
        else:
            image = i_image.copy()
        assert image.dtype == np.uint8
        assert isinstance(image, np.ndarray)
        assert len(image.shape) in (2, 3)
        image = Image.fromarray(np.squeeze(image)).resize(tsize)
        image = np.asarray(image, dtype=np.uint8)
        'Make conventional 3-channel images'
        if len(image.shape) == 2:
            image = np.expand_dims(image, -1)
        else:
            assert len(image.shape) == 3
        return image

    @staticmethod
    def resize_mask(i_mask=None, i_tsize=(128, 128)):
        """i_image is a mask that contain mask for object with index ranging from 0 to N, where 0 stands for background"""
        assert isinstance(i_mask, np.ndarray)
        assert len(i_mask.shape) in (2, 3)
        if len(i_mask.shape) == 2:
            pass
        else:
            assert i_mask.shape[-1] == 1
            i_mask = np.squeeze(i_mask)
        min_val = np.min(i_mask)
        assert min_val == 0
        max_val = np.max(i_mask)
        assert max_val > min_val
        'Start resizing image data'
        rmask = None
        for label in range(1, max_val + 1):
            label_image = 255 * (i_mask == label).astype(np.uint8)
            if np.sum(label_image) == 0:
                continue
            else:
                pass
            label_image = ImageUtils.resize(i_image=label_image, i_tsize=i_tsize)
            label_image = label * (label_image > 0).astype(np.int32)
            if rmask is None:
                rmask = label_image.copy()
            else:
                rmask = rmask + label_image
        return rmask
if __name__ == '__main__':
    print('This module is to implement conventional image processing techniques in Python')
    example_image = ImageUtils.get_gp_image(0)
    rimage = ImageUtils.resize(example_image)
    res_image = ImageUtils.resize(rimage, example_image.shape[0:2])
    plt.subplot(1, 4, 1)
    plt.imshow(example_image, cmap='gray')
    plt.subplot(1, 4, 2)
    plt.imshow(rimage, cmap='gray')
    plt.subplot(1, 4, 3)
    plt.imshow(res_image, cmap='gray')
    plt.subplot(1, 4, 4)
    res_image = np.squeeze(res_image)
    plt.imshow(res_image - example_image, cmap='gray')
    plt.show()
'=================================================================================================================='