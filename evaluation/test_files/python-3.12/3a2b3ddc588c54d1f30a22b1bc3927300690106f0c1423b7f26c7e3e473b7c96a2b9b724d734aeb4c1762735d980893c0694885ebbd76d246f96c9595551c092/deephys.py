from cbor2 import dump
from dataclasses import dataclass, asdict
from typing import List, Optional, Mapping, Union, Dict
import numpy as np
import struct
from time import time
from tqdm import tqdm
import importlib
float32 = lambda val: struct.pack('!f', val)
float64 = lambda val: struct.pack('!d', val)

@dataclass
class Neuron:
    pass

@dataclass
class Layer:
    layerID: str
    neurons: List[Neuron]

@dataclass
class DeephysData:
    name: str

    def save(self):
        fileName = f'{self.name}.{self.extension}'
        print(f'Saving data to {fileName}...')
        with open(fileName, 'wb') as fp:
            dump(asdict(self), fp)
        print(f'done saving data to {fileName}')

@dataclass
class Model(DeephysData):
    """

    :param name: name of the model (e.g.: `"resnet18"`)
    :param layers: A List of layers in the model.
    :param classification_layer: The name of the classification layer. Must be one of the layers defined in `layers`.
    """
    layers: List[Layer]
    classification_layer: str

    def __post_init__(self):
        self.extension = f'model'
        if self.classification_layer not in map(lambda l: l.layerID, self.layers):
            raise Exception(f'classification_layer must be one of the included layers')
        if len(self.name) > 40:
            raise Exception(f'Name of the model too long. Must be 40 characters or less')
        for layer in self.layers:
            if len(layer.layerID) > 30:
                raise Exception(f'Name of the layer {layer.layerID} is too long.')
            if len(layer.neurons) < 0:
                raise Exception(f'Number of neurons in {layer} should be positive, but it was {len(layer.neurons)}')

    def state(self, activations, dtype):
        if len(activations) != len(self.layers):
            raise Exception(f'expected activations data with length of {len(self.layers)} (number of layers) but got {len(activations)}')
        if dtype == 'float32':
            b = 4
        elif dtype == 'float64':
            b = 8
        else:
            raise Exception(f'invalid dtype: {dtype}')
        for index, sub in enumerate(activations):
            subLen = len(sub) / b
            neuronsLen = len(self.layers[index].neurons)
            if subLen != neuronsLen:
                raise Exception(f'expected activations data with length of {neuronsLen} (number of neurons in layer {index}) but got {subLen / b}')
        ms = self.ModelState(activations)
        return ms

    @dataclass
    class ModelState:
        activations: List[bytearray]

def model(model_name: str, layers: Dict[str, int], classification_layer: str):
    """

    :param model_name: The name of the model
    :param layers: A dictionary with the names and number of neurons of each layer.
    :param classification_layer: The name of the classification layer. Must be the name of one of the layers defined in `layers`.
    """
    return Model(name=model_name, layers=list(map(lambda item: Layer(layerID=item[0], neurons=[Neuron()] * item[1]), layers.items())), classification_layer=classification_layer)

def _to_np(d):
    if isinstance(d, list):
        return np.array(d)
    if importlib.util.find_spec('torch') is not None:
        import torch
        if torch.is_tensor(d):
            return d.cpu().detach().numpy()
    return d

def _to_list(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if importlib.util.find_spec('torch') is not None:
        import torch
        if isinstance(value, torch.IntTensor):
            return value.tolist()
    return value

def test(name: str, category_names: list, neural_activity: Dict[str, Union[list, np.ndarray]], model: Model, images: Union[list, np.ndarray], groundtruth: Union[List[int], np.ndarray], dtype: str='float32'):
    """
    Prepare test results for Deephys. The order of the images should be consistent with the order of the groundtruth_categories per image and the neural_activity.

    :param name: The name of the test
    :param category_names: an ordered list of strings representing class names
    :param neural_activity: A dictionary with the name of the layers and their neural activity. The neural activity is an ordered array or list of floats [#images,#neurons]. Length of activations must be the same as the number of images and in the same order.
    :param model: The model structure
    :param images: An ordered list of image pixel data [#images,#channels,dim1,dim2] or [#images,dim1,dim2] for greyscale. Pixels must be floats within the range 0.0:1.0
    :param groundtruth: An ordered list of the ground truth category of each image. The length should be the same as the number of images. Each element should be an integer indicating the index of the category.
    :param dtype: The data type to save activation data as: "float32" or "float64". "float64" is more precise but results in data files almost twice as large. "float64" may also be slower in the app. The input type does not matter, it will get converted to the type in this argument. Default: "float32")
                  Default: ``"float32"``
    :return: a formatted data object which may be saved to a file
    :rtype: deephys.deephys.Test
    """
    if len(name) > 40:
        raise Exception(f'Name of the test must be 40 characters or less')
    layer_names_in_model = []
    for layer in model.layers:
        layer_names_in_model.append(layer.layerID)
    layer_names_in_model = set(layer_names_in_model)
    layer_names_in_state = set(neural_activity.keys())
    if not layer_names_in_model == layer_names_in_state:
        raise Exception(f'Layers names are different from the layers of the model')
    for layer in neural_activity:
        neural_activity[layer] = _to_np(neural_activity[layer])
    for layer in model.layers:
        if layer.layerID == model.classification_layer:
            if len(layer.neurons) != len(category_names):
                raise Exception(f'classification layer must have the same length as the number of classes. classification layer length = {len(layer.neurons)}, classes length = {len(category_names)}')
        elif np.any(neural_activity[layer.layerID] < 0):
            raise Exception(f'Found negative activity in {layer.layerID}. Activity should be taken after ReLU')
        dim_activity = np.shape(neural_activity[layer.layerID])
        if not len(dim_activity) == 2:
            raise Exception(f'Neural activity of {layer.layerID} should be 2 dimensions (number of images x number of neurons)')
        if not dim_activity[0] == len(images):
            raise Exception(f'Neural activity of {layer.layerID} contains {dim_activity[0]} images, but it must be {len(images)} images')
        if not dim_activity[1] == len(layer.neurons):
            raise Exception(f'Neural activity of {layer.layerID} has {dim_activity[1]} neurons but the model was defined with {len(layer.neurons)} neurons')
    if importlib.util.find_spec('torch') is not None:
        import torch
        if isinstance(groundtruth, torch.FloatTensor):
            raise Exception(f'groundtruth should be a list-like of ints, but got a FloatTensor. Please make it an IntTensor.')
    groundtruth = _to_list(groundtruth)
    if any((not isinstance(val, (int, np.uint)) for val in groundtruth)):
        raise Exception(f'ground_truths should be a list-like of ints. Please make it an int.')
    if len(groundtruth) != len(images):
        raise Exception(f'ground_truths length ({len(groundtruth)}) must be same as the image length ({len(images)})')
    images = _to_np(images)
    if len(images.shape) == 3:
        images = np.unsqueeze(images, 1)
        images = images.repeat(1, 3, 1, 1)
    if len(images.shape) != 4:
        raise Exception(f'pixel_data should be a 3D or 4D array-like collection. Colored: [images,channels,dim1,dim2] or greyscale: [images,dim1,dim2], but a shape of {images.shape} was received')
    if images.shape[1] != 3:
        raise Exception(f'pixel_data should have 3 color channels, but {images.shape[1]} were received')
    print('Preparing data...')
    imageList = []
    for i in tqdm(range(len(images))):
        image = images[i]
        target = groundtruth[i]
        mn = np.min(image)
        mx = np.max(image)
        if mx > 1 or mn < 0:
            raise Exception(f'image pixel values must be floats between 0 and 1, but values given range from {mn} to {mx}')
        image = image * 255
        chan_to_bytes = lambda chan: [bytes(row) for row in chan]
        im_to_bytes = lambda im: list(map(chan_to_bytes, im))
        im_as_list = image.astype(np.uint8).tolist()
        im_activations = [neural_activity[layer.layerID][i, :] for layer in model.layers]
        if dtype == 'float32':
            float_fun = float32
        elif dtype == 'float64':
            float_fun = float64
        else:
            raise Exception(f"dtype must be 'float32' or 'float64'. Input was '{dtype}'")
        imageList.append(ImageFile(imageID=i, categoryID=target, category=category_names[target], data=im_to_bytes(im_as_list), activations=model.state(list(map(lambda layer: bytearray([b for a in layer for b in float_fun(a)]), im_activations)), dtype), features=None))
    test = Test(name=name, classes=category_names, dtype=dtype, images=imageList)
    return test

@dataclass
class ImageFile:
    imageID: int
    categoryID: int
    category: str
    data: List[bytearray]
    features: Optional[Mapping[str, str]]
    activations: Model.ModelState

@dataclass
class Test(DeephysData):
    dtype: Optional[str]
    classes: List[str]
    images: List[ImageFile]

    def __post_init__(self):
        self.extension = f'test'

class Stopwatch:

    def __init__(self, name):
        self.name = name

    def start(self):
        self.start_time = time()

    def stop(self):
        self.stop_time = time()
        self.duration_secs = self.stop_time - self.start_time

    def report(self):
        print(f'{self.name} took {self.duration_secs} seconds')

    def stop_and_report(self):
        self.stop(null)
        self.report(null)

def start_stopwatch(name):
    sw = Stopwatch(name)
    sw.start()
    return sw