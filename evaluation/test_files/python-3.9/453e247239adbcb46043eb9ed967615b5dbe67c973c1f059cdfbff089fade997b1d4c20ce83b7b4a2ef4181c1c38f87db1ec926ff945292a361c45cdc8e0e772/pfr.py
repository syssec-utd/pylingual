__all__ = ['ROOT', 'PinterestFaces']
from fastai.vision.all import *
import fastai_datasets.patches
from .utils import *
ROOT = data_path() / '105_classes_pins_dataset'

def PinterestFaces(mtcnn=True):
    """Requires the user to download the file manually"""
    assert ROOT.exists(), f'Please manually download the dataset to {ROOT}'
    dblock = DataBlock(blocks=(ImageBlock, CategoryBlock), get_items=get_image_files, get_y=lambda p: parent_label(p).replace('pins_', '').replace('_', ' ').title())
    return dblock.datasets(mtcnn_aligned(ROOT, batched=False) if mtcnn else ROOT)