from abc import abstractmethod
from typing import Hashable, List, Sequence, Optional
from fuse.data.utils.sample import get_sample_id
from fuse.utils import NDict
from fuse.data import OpBase
import numpy
import torch

class OpDebugBase(OpBase):
    """
    Base class for debug operations.
    Provides the ability to limit samples to debug (will debug the first k samples).
    Inherits and implements self.call_debug instead of self.__call__.
    """

    def __init__(self, name: Optional[str]=None, sample_ids: Optional[List[Hashable]]=None, num_samples: int=0):
        """
        :param name: string identifier - might be useful when the debug op display or save information into a file
        :param sample_ids: apply for the specified sample ids. To apply for all set to None.
        :param num_samples: apply for the first num_samples (per process). if 0, will apply for all.
        """
        super().__init__()
        self._name = name
        self._sample_ids = sample_ids
        self._num_samples = num_samples
        self._num_samples_done = 0

    def reset(self, name: Optional[str]=None):
        """Reset operation state"""
        self._num_samples_done = 0
        self._name = name

    def should_debug_sample(self, sample_dict: NDict) -> bool:
        if self._num_samples and self._num_samples_done >= self._num_samples:
            return False
        if self._sample_ids is not None:
            sid = get_sample_id(sample_dict)
            if sid not in self._sample_ids:
                return False
        self._num_samples_done += 1
        return True

    def __call__(self, sample_dict: NDict, **kwargs) -> NDict:
        if self.should_debug_sample(sample_dict):
            self.call_debug(sample_dict, **kwargs)
        return sample_dict

    @abstractmethod
    def call_debug(self, sample_dict: NDict, **kwargs) -> None:
        """The actual debug op implementation"""
        raise NotImplementedError

class OpPrintKeys(OpDebugBase):
    """
    Print list of available keys at a given point in the data pipeline
    It's recommended, but not a must, to run it in a single process.
    ```
    from fuse.utils.utils_debug import FuseDebug
    FuseDebug("debug")
    ```

    Example:
    ```
    (OpPrintKeys(num_samples=1), dict()),
    ```
    """

    def call_debug(self, sample_dict: NDict) -> None:
        print(f'Sample {get_sample_id(sample_dict)} keys:')
        for key in sample_dict.keypaths():
            print(f'\t{key}')

class OpPrintShapes(OpDebugBase):
    """
    Print the shapes/length of every torch tensor / numpy array / sequence
    Add at the top your script to force single process:
    ```
    from fuse.utils.utils_debug import FuseDebug
    FuseDebug("debug")
    ```
    Example:
    ```
    (OpPrintShapes(num_samples=1), dict()),
    ```
    """

    def call_debug(self, sample_dict: NDict) -> None:
        print(f'Sample {get_sample_id(sample_dict)} shapes:')
        for key in sample_dict.keypaths():
            value = sample_dict[key]
            if isinstance(value, torch.Tensor):
                print(f'\t{key} is tensor with shape: {value.shape}')
            elif isinstance(value, numpy.ndarray):
                print(f'\t{key} is numpy array with shape: {value.shape}')
            elif not isinstance(value, str) and isinstance(value, Sequence):
                print(f'\t{key} is sequence with length: {len(value)}')

class OpPrintTypes(OpDebugBase):
    """
    Print the the type of each key

    Add at the top your script to force single process:
    ```
    from fuse.utils.utils_debug import FuseDebug
    FuseDebug("debug")
    ```
    Example:
    ```
    (OpPrintTypes(num_samples=1), dict()),
    ```
    """

    def call_debug(self, sample_dict: NDict) -> None:
        print(f'Sample {get_sample_id(sample_dict)} types:')
        for key in sample_dict.keypaths():
            value = sample_dict[key]
            print(f'\t{key} - {type(value).__name__}')

class OpPrintKeysContent(OpDebugBase):
    """
    Print sample's keys and contents.
    It's recommended, but not a must, to run it in a single process.
    ```
    from fuse.utils.utils_debug import FuseDebug
    FuseDebug("debug")
    ```
    Example:
    ```
    (OpPrintKeysContent(num_samples=1), dict(keys=["data.input.mri_path", "data.label"])),
    (OpPrintKeysContent(num_samples=1), dict(keys=None)),
    ```
    """

    def call_debug(self, sample_dict: NDict, keys: List[str]) -> None:
        """
        :param keys: List of keys to print. Set to 'None' to print all keys.
        """
        print(f"OpPrintKeysContent, sample '{get_sample_id(sample_dict)}', <key> = <content>:")
        dict_keys = sample_dict.keypaths()
        if keys is None:
            keys = dict_keys
        for key in keys:
            if key in dict_keys:
                print(f'\t{key} = {sample_dict[key]}')
            else:
                print(f'\tWARNING! {key} not in sample_dict')