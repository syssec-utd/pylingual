"""Classes for data loading and processing.

Defines Tasks, TaskRegistry, Mixture, and MixtureRegistry
"""
import abc
import collections
import dataclasses
import functools
import inspect
import json
import os
import re
from typing import Any, Callable, Iterable, Mapping, MutableMapping, Optional, Sequence, Tuple, Type, Union, List
from absl import logging
import clu.metrics
import numpy as np
from packaging import version
from seqio import metrics as metrics_lib
from seqio import preprocessors as seqio_preprocessors
from seqio import utils
from seqio.feature_converters import FeatureConverter
from seqio.vocabularies import PassThroughVocabulary
from seqio.vocabularies import Vocabulary
import tensorflow.compat.v2 as tf
import tensorflow_datasets as tfds
import typing_extensions
_DEFAULT_FEATURE_KEYS = ['inputs', 'targets']
_VALID_TASK_NAME_REGEX = re.compile('^[\\w\\d\\.\\:_]+$')
_MAX_EXAMPLES_TO_MEM_CACHE = 10000
SHUFFLE_BUFFER_SIZE = 1000
DatasetReaderType = Callable[[Union[str, Iterable[str]]], tf.data.Dataset]
DecodeFnType = Callable[..., Mapping[str, tf.train.Feature]]
Feature = utils.Feature

@dataclasses.dataclass(frozen=True)
class ContinuousFeature(Feature):
    """A container for multi-modal output features of data providers."""
    vocabulary: Vocabulary = PassThroughVocabulary(size=0)
    add_eos: bool = False

@dataclasses.dataclass(frozen=True)
class ShardInfo:
    """A container for specifying sharding info."""
    index: int
    num_shards: int

class DatasetProviderBase(metaclass=abc.ABCMeta):
    """Abstract base for classes that provide a tf.data.Dataset."""

    @abc.abstractproperty
    def output_features(self) -> Mapping[str, Feature]:
        raise NotImplementedError

    @abc.abstractproperty
    def splits(self) -> Sequence[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_dataset(self, sequence_length: int, split: str, use_cached: bool=False, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None, num_epochs: int=1) -> tf.data.Dataset:
        """Returns the requested tf.data.Dataset."""
        raise NotImplementedError

    @abc.abstractmethod
    def num_input_examples(self, split: str) -> int:
        raise NotImplementedError

class DatasetProviderRegistry(object):
    """Base for registry of data providers.

  Subclasses must wrap `get` method to override the return type for pytype.
  TODO(adarob): Remove the need to override `get`.
  """
    _REGISTRY: MutableMapping[str, DatasetProviderBase]
    _PROVIDER_TYPE: Type[DatasetProviderBase]

    @classmethod
    def add_provider(cls, name: str, provider):
        """Adds a data provider instance to the registry."""
        if name in cls._REGISTRY:
            raise ValueError('Attempting to register duplicate provider: %s' % name)
        if not isinstance(provider, cls._PROVIDER_TYPE):
            raise ValueError('Attempting to register a class of an invalid type. Expecting instance of %s, got %s' % (cls._PROVIDER_TYPE, type(provider).__name__))
        cls._REGISTRY[name] = provider

    @classmethod
    def add(cls, name: str, provider_cls, provider_kwargs):
        """Instantiates and adds provider to the registry."""
        if not issubclass(provider_cls, cls._PROVIDER_TYPE):
            raise ValueError('Attempting to register a class of an invalid type. Expecting instance of %s, got %s' % (cls._PROVIDER_TYPE, provider_cls))
        provider = provider_cls(**provider_kwargs)
        cls.add_provider(name, provider)
        return provider

    @classmethod
    def remove(cls, name):
        """Remove provider from the registry, if it exists."""
        if name in cls._REGISTRY:
            del cls._REGISTRY[name]

    @classmethod
    def get(cls, name):
        """Returns provider from the registry."""
        if name not in cls._REGISTRY:
            raise ValueError('Provider name not registered: %s' % name)
        return cls._REGISTRY[name]

    @classmethod
    def names(cls):
        """Returns all provider names in registry."""
        return cls._REGISTRY.keys()

    @classmethod
    def reset(cls):
        """Removes all of the registered tasks."""
        cls._REGISTRY = {}

    @classmethod
    def get_dataset(cls, name, sequence_length, split, use_cached=False, shuffle=True, seed=None, shard_info=None, num_epochs=1):
        """Returns the requested tf.data.Dataset."""
        return cls.get(name).get_dataset(sequence_length=sequence_length, split=split, use_cached=use_cached, shuffle=shuffle, seed=seed, shard_info=shard_info, num_epochs=num_epochs)

class DataSourceInterface(typing_extensions.Protocol):
    """Interface for DataSource."""

    def num_input_examples(self, split: str) -> int:
        ...

    @property
    def caching_permitted(self) -> bool:
        ...

    @property
    def splits(self) -> Sequence[str]:
        ...

    @property
    def supports_arbitrary_sharding(self) -> bool:
        ...

    @property
    def output_features(self) -> Mapping[str, Feature]:
        ...

    def list_shards(self, split: str) -> Sequence[str]:
        ...

    def get_dataset(self, split: str, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None) -> tf.data.Dataset:
        ...

class DataSource(DatasetProviderBase):
    """A `DatasetProvider` that provides raw data from an input source.

  Inherits all abstract methods and properties of `DatasetProviderBase` except
  those overidden below.
  """

    def __init__(self, splits: Iterable[str], num_input_examples: Optional[Mapping[str, int]]=None, caching_permitted: bool=True):
        self._splits = tuple(splits)
        self._num_input_examples = dict(num_input_examples) if num_input_examples is not None else None
        self._caching_permitted = caching_permitted

    @property
    def caching_permitted(self) -> bool:
        """Indicates whether this data source may be cached.

    Caching may be prohibited for the sake of data versioning rigor or as a
    matter of policy for certain datasets.
    """
        return self._caching_permitted

    @property
    def splits(self) -> Sequence[str]:
        return self._splits

    @abc.abstractproperty
    def supports_arbitrary_sharding(self) -> bool:
        """Whether supports sharding beyond those available in `list_shards`."""
        raise NotImplementedError

    @property
    def output_features(self) -> Mapping[str, Feature]:
        """Override unused property of `DatasetProviderBase`."""
        raise NotImplementedError

    @abc.abstractmethod
    def list_shards(self, split: str) -> Sequence[str]:
        """Returns string identifiers of input shards."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_dataset(self, split: str, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None) -> tf.data.Dataset:
        """Overrides base class to add shard identifier and remove use_cached.

    Args:
      split: string, the split to return.
      shuffle: bool, whether to shuffle the input source.
      seed: tf.int64 scalar tf.Tensor (or None) for shuffling input source.
      shard_info: optional specification for loading a shard of the split.
    """
        raise NotImplementedError

    def num_input_examples(self, split: str) -> Optional[int]:
        if self._num_input_examples is None:
            return None
        return self._num_input_examples[split]

def _get_name(function):
    """Returns the name of a (possibly partially applied) function."""
    if isinstance(function, functools.partial):
        return function.func.__name__
    else:
        return function.__name__

def _validate_args(fn, expected_pos_args):
    """Ensure function has exactly expected positional args."""
    argspec = inspect.getfullargspec(fn)
    expected_pos_args = tuple(expected_pos_args)
    actual_args = tuple(argspec.args)
    if actual_args[:len(expected_pos_args)] != expected_pos_args:
        raise ValueError("'%s' must have positional args %s, got: %s" % (_get_name(fn), expected_pos_args, actual_args))
    actual_pos_args = tuple(argspec.args[:-len(argspec.defaults)] if argspec.defaults else argspec.args)
    if actual_pos_args != expected_pos_args[:len(actual_pos_args)]:
        raise ValueError("'%s' may only have positional args %s, got: %s" % (_get_name(fn), expected_pos_args, actual_pos_args))

class DatasetFnCallable(typing_extensions.Protocol):

    def __call__(self, split: str, shuffle_files: bool, seed: Optional[int]=None) -> tf.data.Dataset:
        ...

class FunctionDataSource(DataSource):
    """A `DataSource` that uses a function to provide the input data.

  This source is not recommended when shuffling is required unless it is
  cached/materialized in advance. Using this source without caching for training
  will result in insufficient shuffling and lead to repeated data on restarts.
  """

    def __init__(self, dataset_fn: DatasetFnCallable, splits: Iterable[str], num_input_examples: Optional[Mapping[str, int]]=None, caching_permitted: bool=True):
        """FunctionDataSource constructor.

    Args:
      dataset_fn: a function with the signature `dataset_fn(split,
        shuffle_files)' (and optionally the variable `seed`) that returns a
        `tf.data.Dataset`.
      splits: an iterable of applicable string split names.
      num_input_examples: dict or None, an optional dictionary mapping split to
        its size in number of input examples (before preprocessing). The
        `num_input_examples` method will return None if not provided.
      caching_permitted: indicates whether this data source may be cached.
        Default True.
    """
        _validate_args(dataset_fn, ['split', 'shuffle_files'])
        self._dataset_fn = dataset_fn
        super().__init__(splits=splits, num_input_examples=num_input_examples, caching_permitted=caching_permitted)

    @property
    def supports_arbitrary_sharding(self) -> bool:
        return False

    def get_dataset(self, split: str, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None) -> tf.data.Dataset:
        if shard_info and shard_info.num_shards > 1:
            raise ValueError('`FunctionDataSource` does not support low-level sharding. Use tf.data.Dataset.shard instead.')
        if shuffle:
            logging.warning('Using an uncached FunctionDataset for training is not recommended since it often results in insufficient shuffling on restarts, resulting in overfitting. It is highly recommended that you cache this task before training with it or use a data source that supports lower-level shuffling (e.g., FileDataSource).')
        if seed is None:
            ds = self._dataset_fn(split=split, shuffle_files=shuffle)
        else:
            _validate_args(self._dataset_fn, ['split', 'shuffle_files', 'seed'])
            ds = self._dataset_fn(split=split, shuffle_files=shuffle, seed=seed)
        return ds

    def list_shards(self, split: str) -> Sequence[str]:
        return [split]

class TfdsDataSource(DataSource):
    """A `DataSource` that uses TensorFlow Datasets to provide the input data."""

    def __init__(self, tfds_name: str, tfds_data_dir: Optional[str]=None, splits: Optional[Union[Iterable[str], Mapping[str, str]]]=None, caching_permitted: bool=True, decoders: Optional[tfds.typing.TreeDict[tfds.decode.Decoder]]=None):
        """TfdsTask constructor.

    Args:
      tfds_name: The name and version number of a TFDS dataset,
        optionally with a config.
      tfds_data_dir: An optional path to a specific TFDS data directory to use.
        If provided `tfds_name` must be a valid dataset in the directory.
        If `tfds_name` is empty `tfds_dara_dir` must point to the directory with
        one dataset.
      splits: an iterable of allowable string split names, a dict mapping
        allowable canonical splits (e.g., 'validation') to TFDS splits or slices
        (e.g., 'train[':1%']), or None. The default, None, uses all available
          splits from the TFDS dataset info.
      caching_permitted: indicates whether this data source may be cached.
        Default True.
      decoders: dict (optional), mapping from features to tfds.decode.Decoders,
        such as tfds.decode.SkipDecoding() for skipping image byte decoding
    """
        if tfds_name and ':' not in tfds_name:
            raise ValueError(f'TFDS name must contain a version number, got: {tfds_name}')
        if splits and (not isinstance(splits, dict)):
            splits = {k: k for k in splits}
        self._tfds_dataset = utils.LazyTfdsLoader(tfds_name, data_dir=tfds_data_dir, split_map=splits if isinstance(splits, dict) else None, decoders=decoders)
        super().__init__(splits=splits or (), caching_permitted=caching_permitted)

    @property
    def splits(self):
        """Overrides since we can't call `info.splits` until after init."""
        return self._splits or self._tfds_dataset.info.splits

    @property
    def tfds_dataset(self):
        return self._tfds_dataset

    @property
    def supports_arbitrary_sharding(self) -> bool:
        return False

    def get_dataset(self, split: str, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None) -> tf.data.Dataset:
        return self.tfds_dataset.load(split, shuffle_files=shuffle, seed=seed, shard_info=shard_info)

    def num_input_examples(self, split: str) -> int:
        """Overrides since we can't call `info.splits` until after init."""
        return self.tfds_dataset.size(split)

    def list_shards(self, split: str) -> Sequence[str]:

        def _get_filename(info):
            if isinstance(info, dict):
                return info['filename']
            return info.filename
        return [_get_filename(info) for info in self.tfds_dataset.files(split)]

class FileDataSource(DataSource):
    """A `DataSource` that reads a file to provide the input dataset."""

    def __init__(self, read_file_fn: Callable[[tf.data.Dataset], tf.data.Dataset], split_to_filepattern: Mapping[str, Union[str, Iterable[str]]], num_input_examples: Optional[Mapping[str, int]]=None, caching_permitted: bool=True, file_shuffle_buffer_size: Optional[int]=None):
        """FileDataSource constructor.

    Args:
      read_file_fn: a callable for creating a `tf.data.Dataset` from a
        `tf.data.Dataset` of file paths, e.g., `tf.data.TFRecordDataset`.
      split_to_filepattern: a mapping from split names to filepatterns to be
        expanded with glob.
      num_input_examples: dict or None, an optional dictionary mapping split to
        its size in number of input examples (before preprocessing). The
        `num_input_examples` method will return None if not provided.
      caching_permitted: indicates whether this data source may be cached.
        Default True.
      file_shuffle_buffer_size: The buffer size to shuffle files when needed. If
        None, the number of files is used as buffer size for a perfect shuffle
        (default and recommended). A value of 16 may be explicitly set to
        replicate earlier behavior.
    """
        self._split_to_filepattern = split_to_filepattern
        self._reader = read_file_fn
        self._file_shuffle_buffer_size = file_shuffle_buffer_size
        super().__init__(splits=split_to_filepattern.keys(), num_input_examples=num_input_examples, caching_permitted=caching_permitted)

    @property
    def supports_arbitrary_sharding(self) -> bool:
        return False

    def get_dataset(self, split: str, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None) -> tf.data.Dataset:
        files = self.list_shards(split)
        if not files:
            raise ValueError(f'No file is found for the file pattern: {self._split_to_filepattern[split]}.')
        files_ds = tf.data.Dataset.from_tensor_slices(np.array(files, dtype=str))
        if shard_info:
            if len(files) < shard_info.num_shards:
                raise ValueError(f'Dataset has too few files to shard. {len(files)} files vs {shard_info.num_shards} shards requested.')
            files_ds = files_ds.shard(shard_info.num_shards, shard_info.index)
        if shuffle:
            if self._file_shuffle_buffer_size:
                logging.warning('`file_shuffle_buffer_size` is explicitly set to %d; this may lead to an imperfect file shuffle. Leave `file_shuffle_buffer_size` unset for a perfect shuffle.', self._file_shuffle_buffer_size)
            file_shuffle_buffer_size = self._file_shuffle_buffer_size or len(files)
            files_ds = files_ds.shuffle(buffer_size=file_shuffle_buffer_size, seed=seed)
        return files_ds.interleave(self._reader, cycle_length=16, block_length=16, num_parallel_calls=tf.data.experimental.AUTOTUNE)

    def list_shards(self, split: str) -> Sequence[str]:
        return tf.io.gfile.glob(self._split_to_filepattern[split])

class TextLineDataSource(FileDataSource):
    """A `FileDataSource` that reads lines of text from a file as input."""

    def __init__(self, split_to_filepattern: Mapping[str, Union[str, Iterable[str]]], skip_header_lines: int=0, num_input_examples: Optional[Mapping[str, int]]=None, caching_permitted: bool=True, file_shuffle_buffer_size: Optional[int]=None):
        """TextLineDataSource constructor.

    Args:
      split_to_filepattern: a mapping from split names to filepatterns to be
        expanded with glob.
      skip_header_lines: int, number of header lines to skip in each source
        file.
      num_input_examples: dict or None, an optional dictionary mapping split to
        its size in number of input examples (before preprocessing). The
        `num_input_examples` method will return None if not provided.
      caching_permitted: indicates whether this data source may be cached.
        Default True.
      file_shuffle_buffer_size: The buffer size to shuffle files when needed. If
        None, the number of files is used as buffer size for a perfect shuffle
        (default and recommended). A value of 16 may be explicitly set to
        replicate earlier behavior.
    """
        self._skip_header_lines = skip_header_lines

        def read_file_fn(filepattern):
            return tf.data.TextLineDataset(filepattern).skip(skip_header_lines)
        super().__init__(read_file_fn=read_file_fn, split_to_filepattern=split_to_filepattern, num_input_examples=num_input_examples, caching_permitted=caching_permitted, file_shuffle_buffer_size=file_shuffle_buffer_size)

class TFExampleDataSource(FileDataSource):
    """A `FileDataSource` that reads files of tf.train.Example protos as input."""

    def __init__(self, split_to_filepattern: Mapping[str, Union[str, Iterable[str]]], feature_description: Mapping[str, Union[tf.io.FixedLenFeature, tf.io.VarLenFeature]], reader_cls: DatasetReaderType=tf.data.TFRecordDataset, num_input_examples: Optional[Mapping[str, int]]=None, caching_permitted: bool=True, file_shuffle_buffer_size: Optional[int]=None):
        """TFExampleDataSource constructor.

    Args:
      split_to_filepattern: dict of string (split name) to either string
        (filename or filepattern) or list of strings (filenames or
        filepatterns).
      feature_description: dict, a mapping of string feature keys to
        `tf.io.FixedLenFeature` or `tf.io.VarLenFeature` values.
      reader_cls: `tf.data.Dataset`, a dataset class to read the input files.
      num_input_examples: dict or None, an optional dictionary mapping split to
        its size in number of input examples (before preprocessing). The
        `num_input_examples` method will return None if not provided.
      caching_permitted: indicates whether this data source may be cached.
        Default True.
      file_shuffle_buffer_size: The buffer size to shuffle files when needed. If
        None, the number of files is used as buffer size for a perfect shuffle
        (default and recommended). A value of 16 may be explicitly set to
        replicate earlier behavior.
    """

        def parse_fn(*args):
            pb = args[-1]
            return tf.io.parse_single_example(pb, feature_description)

        def read_file_fn(filepattern):
            return reader_cls(filepattern).map(parse_fn, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        self.reader_cls = reader_cls
        self.parse_fn = parse_fn
        super().__init__(read_file_fn=read_file_fn, split_to_filepattern=split_to_filepattern, num_input_examples=num_input_examples, caching_permitted=caching_permitted, file_shuffle_buffer_size=file_shuffle_buffer_size)

class ProtoDataSource(FileDataSource):
    """A `FileDataSource` that reads files of arbitrary protos as input."""

    def __init__(self, split_to_filepattern: Mapping[str, Union[str, Iterable[str]]], decode_proto_fn: DecodeFnType, reader_cls: DatasetReaderType=tf.data.TFRecordDataset, num_input_examples: Optional[Mapping[str, int]]=None, caching_permitted: bool=True, file_shuffle_buffer_size: Optional[int]=None):
        """ProtoDataSource constructor.

    Args:
      split_to_filepattern: dict of string (split name) to either string
        (filename or filepattern) or list of strings (filenames or
        filepatterns).
      decode_proto_fn: a callable to parse a serialized proto to features.
      reader_cls: `tf.data.Dataset`, a dataset class to read the input files.
      num_input_examples: dict or None, an optional dictionary mapping split to
        its size in number of input examples (before preprocessing). The
        `num_input_examples` method will return None if not provided.
      caching_permitted: indicates whether this data source may be cached.
        Default True.
      file_shuffle_buffer_size: The buffer size to shuffle files when needed. If
        None, the number of files is used as buffer size for a perfect shuffle
        (default and recommended). A value of 16 may be explicitly set to
        replicate earlier behavior.
    """

        def read_file_fn(filepattern: Union[str, Iterable[str]]):
            return reader_cls(filepattern).map(decode_proto_fn, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        super().__init__(read_file_fn=read_file_fn, split_to_filepattern=split_to_filepattern, num_input_examples=num_input_examples, caching_permitted=caching_permitted, file_shuffle_buffer_size=file_shuffle_buffer_size)

def _rename_plaintext_to_pretokenized(dataset: tf.data.Dataset) -> tf.data.Dataset:
    """Rename cached _plaintext features to new _pretokenized standard."""

    def _rename(inputs):
        outputs = {}
        for k, v in inputs.items():
            if k.endswith('_plaintext'):
                k = k[:-len('plaintext')] + 'pretokenized'
            outputs[k] = v
        return outputs
    return dataset.map(_rename, num_parallel_calls=tf.data.experimental.AUTOTUNE)

class _CachedDataSource(FileDataSource):
    """A `FileDataSource` for reading datasets cached offline."""

    def __init__(self, cache_dir: str, split: str, file_shuffle_buffer_size: Optional[int]=None):
        with tf.io.gfile.GFile(utils.get_cached_info_path(cache_dir, split)) as f:
            split_info = json.load(f)
            features = split_info['features']
        with tf.io.gfile.GFile(utils.get_cached_stats_path(cache_dir, split)) as f:
            stats = json.load(f)
        version_when_cached = version.Version(split_info.get('seqio_version', '0.pre'))
        version_with_true_dtypes = version.Version('0.0.0')
        if version_when_cached < version_with_true_dtypes:
            for name, feat in features.items():
                if feat['dtype'] == 'int64':
                    logging.info("Casting cached '%s' to int32.", name)
                    feat['dtype'] = 'int32'

        def _feature_config(shape, dtype):
            if dtype in ('int32', 'bool'):
                dtype = 'int64'
            if shape and shape[0] is None:
                return tf.io.FixedLenSequenceFeature(shape[1:], dtype, allow_missing=True)
            return tf.io.FixedLenFeature(shape, dtype)
        feature_description = {feat: _feature_config(**desc) for feat, desc in features.items()}

        def read_file_fn(filepattern):
            ds = tf.data.TFRecordDataset(filepattern)
            ds = ds.map(lambda pb: tf.io.parse_single_example(pb, feature_description), num_parallel_calls=tf.data.experimental.AUTOTUNE)
            ds = ds.map(lambda x: {k: tf.cast(v, features[k]['dtype']) for k, v in x.items()}, num_parallel_calls=tf.data.experimental.AUTOTUNE)
            ds = _rename_plaintext_to_pretokenized(ds)
            return ds
        split_to_filepattern = {split: '%s-*-of-*%d' % (utils.get_cached_tfrecord_prefix(cache_dir, split), split_info['num_shards'])}
        super().__init__(read_file_fn=read_file_fn, split_to_filepattern=split_to_filepattern, num_input_examples={split: stats['examples']}, file_shuffle_buffer_size=file_shuffle_buffer_size)

class CacheDatasetPlaceholder(object):
    """A placeholder to signal when in the pipeline offline caching will occur."""

    def __init__(self, required=False, file_shuffle_buffer_size: Optional[int]=None):
        """CacheDatasetPlaceholder constructor.

    Args:
      required: whether the dataset must be accessed in its cached form, and
        on-the-fly preprocessing is disallowed.
      file_shuffle_buffer_size: The buffer size to shuffle files when needed. If
        None, the number of files is used as buffer size for a perfect shuffle
        (default and recommended). A value of 16 may be explicitly set to
        replicate earlier behavior.
    """
        self._required = required
        self._file_shuffle_buffer_size = file_shuffle_buffer_size

    @property
    def required(self):
        return self._required

    @property
    def file_shuffle_buffer_size(self):
        return self._file_shuffle_buffer_size

    def __call__(self, dataset):
        raise RuntimeError('`CacheDatasetPlaceholder` should never be called.')
MetricFnCallable = metrics_lib.MetricFnCallable

class Task(DatasetProviderBase):
    """A class to manage a dataset and its related metrics."""

    def __init__(self, name: str, source: DataSource, output_features: Mapping[str, Feature], preprocessors: Optional[Sequence[Callable[..., tf.data.Dataset]]]=None, postprocess_fn: Optional[Callable[..., Any]]=None, metric_fns: Optional[Sequence[MetricFnCallable]]=None, metric_objs: Optional[Sequence[metrics_lib.Metric]]=None, shuffle_buffer_size: Optional[int]=SHUFFLE_BUFFER_SIZE):
        """Task constructor.

    Args:
      name: a unique name for the Task.
      source: a `DataSource` that provides a raw `tf.data.Dataset`.
      output_features: dict(str, Feature), output features of the Task to be
        passed to the model. After preprocessing, examples will be validated to
        ensure they include features that match this specification. Note that
        additional features may be included (e.g., for evaluation), but they
        will not be passed to the model.
      preprocessors: list(callable), an optional list of functions that receive
        a tf.data.Dataset and return a tf.data.Dataset. These will be executed
        sequentially and the final dataset must include features matching
        `output_features`.
      postprocess_fn: callable, an optional function that receives decoded model
        outputs and converts them to a form that is ready for evaluation using
        the metric functions in `metric_fns`.
      metric_fns: list(callable), an optional list of metric functions with a
        signature that matches one of three possible forms:
        - (targets, scores) - Note that `scores` refers to the score the model
            assigned the target sequence, given the input.
        - (targets, predictions)
        - (targets, predictions, aux_values) - Note that
            `aux_values` refers to a dictionary of auxiliary values that the
            model assigned to each sequence.
        metric_fns are being deprecated, please use metric_objs instead.
      metric_objs: list(clu Metric instances), an optional list of clu Metric
        objects.
      shuffle_buffer_size: an optional integer to set the shuffle buffer size.
        If None, shuffling will be disallowed.
    """
        if not _VALID_TASK_NAME_REGEX.match(name):
            raise ValueError("Task name '%s' contains invalid characters. Must match regex: %s" % (name, _VALID_TASK_NAME_REGEX.pattern))
        metric_fns = metric_fns or []
        metric_objs = metric_objs or []
        if metric_fns:
            metric_objs += [metrics_lib.LegacyMetric.empty(mf, postprocess_fn) for mf in metric_fns]
        self._metric_objs = metric_objs
        self._predict_metric_fns = []
        self._predict_with_aux_metric_fns = []
        self._score_metric_fns = []
        for metric_fn in metric_fns:
            pos_args = tuple((key for key, param in inspect.signature(metric_fn).parameters.items() if param.default == inspect.Parameter.empty))
            if pos_args == ('targets', 'scores'):
                self._score_metric_fns.append(metric_fn)
            elif pos_args == ('targets', 'predictions'):
                self._predict_metric_fns.append(metric_fn)
            elif pos_args == ('targets', 'predictions', 'aux_values'):
                self._predict_with_aux_metric_fns.append(metric_fn)
            else:
                raise ValueError(f"Metric functions must have positional arguments matching either ('targets', 'scores'), ('targets', 'predictions') or ('targets', 'predictions', 'aux_values'). Got: {pos_args}")
        self._name = name
        self._source = source
        preprocessors = tuple(preprocessors or [])
        cache_step_idxs = [i for i, p in enumerate(preprocessors) if isinstance(p, CacheDatasetPlaceholder)]
        if len(cache_step_idxs) > 1:
            raise ValueError(f"`CacheDatasetPlaceholder` can appear at most once in the preprocessing pipeline. Found {len(cache_step_idxs)} in '{name}'.")
        cache_step_idx = cache_step_idxs[0] if cache_step_idxs else None
        if cache_step_idx is not None:
            if not source.caching_permitted:
                raise ValueError(f"Caching was requested for '{name}', but the underlying data source prohibits caching. Please remove `CacheDatasetPlaceholder` and try again.")
            for prep in preprocessors[:cache_step_idx]:
                prep_args = inspect.signature(prep).parameters.keys()
                if 'sequence_length' in prep_args:
                    raise ValueError(f"'{_get_name(prep)}' has a `sequence_length` argument but occurs before `CacheDatasetPlaceholder` in '{name}'. This is not allowed since the sequence length is specified at run time.")
                if 'seed' in prep_args or 'seeds' in prep_args:
                    logging.warning("'%s' has a `seed(s)` argument but occurs before `CacheDatasetPlaceholder` in '%s'. This is not recommended since the same samples will be used each epoch when reading from the cache.", _get_name(prep), name)
        self._cache_step_idx = cache_step_idx
        self._preprocessors = preprocessors
        self._metric_fns = tuple(metric_fns)
        self._postprocess_fn = postprocess_fn
        self._cache_dir = None
        self._stats = {}
        self._shuffle_buffer_size = shuffle_buffer_size
        self._output_features = collections.OrderedDict(sorted(list(output_features.items())))

    @property
    def name(self) -> str:
        return self._name

    @property
    def metric_objs(self) -> Sequence[metrics_lib.Metric]:
        """List of all metric objects."""
        return self._metric_objs

    @property
    def metric_fns(self) -> Sequence[MetricFnCallable]:
        """List of all metric functions."""
        return self._predict_metric_fns + self._score_metric_fns + self._predict_with_aux_metric_fns

    @property
    def score_metric_fns(self) -> Sequence[MetricFnCallable]:
        """List of metric functions that use log likelihood scores."""
        return self._score_metric_fns

    @property
    def predict_metric_fns(self) -> Sequence[MetricFnCallable]:
        """List of metric functions that use model predictions."""
        return self._predict_metric_fns

    @property
    def predict_with_aux_metric_fns(self) -> Sequence[MetricFnCallable]:
        """List of metric functions that use model predictions with aux values."""
        return self._predict_with_aux_metric_fns

    @property
    def output_features(self) -> Mapping[str, Feature]:
        return self._output_features

    @property
    def splits(self) -> Sequence[str]:
        s = self.source.splits
        if not s:
            raise ValueError(f'Task {self.name} has no splits')
        return s

    @property
    def source(self) -> DataSource:
        return self._source

    @property
    def preprocessors(self) -> Sequence[Callable[..., tf.data.Dataset]]:
        return self._preprocessors

    @property
    def postprocessor(self) -> Callable[..., Any]:
        return self._postprocess_fn

    @property
    def shuffle_buffer_size(self) -> int:
        return self._shuffle_buffer_size

    def replace(self, **kwargs):
        """Create a new variant of the current task using properties in kwargs."""
        properties = ['name', 'source', 'output_features', 'preprocessors', 'metric_fns', 'metric_objs', 'shuffle_buffer_size']
        task_kwargs = {}
        for key in properties:
            if key in kwargs:
                value = kwargs[key]
            else:
                value = getattr(self, key)
            task_kwargs[key] = value
        return Task(**task_kwargs)

    def num_input_examples(self, split: str) -> Optional[int]:
        return self.source.num_input_examples(split)

    def _preprocess_dataset(self, dataset: tf.data.Dataset, preprocessors: Sequence[Callable[..., tf.data.Dataset]], sequence_length: Optional[Mapping[str, int]]=None) -> tf.data.Dataset:
        """Sequentially applies preprocessors."""
        for prep_fn in preprocessors:
            prep_fn = utils.add_kwargs_to_transform(prep_fn, sequence_length=sequence_length, output_features=self.output_features)
            dataset = prep_fn(dataset)
        return dataset

    def _validate_preprocessing(self, dataset: tf.data.Dataset) -> tf.data.Dataset:
        """Validates preprocessed dataset, raising Exceptions if needed.

    Args:
      dataset: a tf.data.Dataset to validate.

    Returns:
      a validated tf.data.Dataset.
    """
        actual_specs = dataset.element_spec
        for feat, feat_spec in self.output_features.items():
            if feat not in actual_specs:
                if feat_spec.required:
                    raise ValueError(f'Task dataset is missing expected output feature after preprocessing: {feat}')
                else:
                    continue
            actual_spec = actual_specs[feat]
            if feat_spec.dtype != actual_spec.dtype:
                raise ValueError(f"Task dataset has incorrect type for feature '{feat}' after preprocessing: Got {actual_spec.dtype.name}, expected {feat_spec.dtype.name}")
            if feat_spec.rank != actual_spec.shape.rank:
                raise ValueError(f"Task dataset has incorrect rank for feature '{feat}' after preprocessing: Got {actual_spec.shape.rank}, expected {feat_spec.rank}")
        return dataset

    def _trim_output_features(self, dataset: tf.data.Dataset, sequence_length: Optional[Mapping[str, Union[int, Sequence[int]]]]) -> tf.data.Dataset:
        """Trim output features to sequence length."""
        return utils.trim_dataset(dataset, sequence_length, self.output_features)

    def preprocess_precache(self, dataset: tf.data.Dataset, seed: Optional[int]=None) -> tf.data.Dataset:
        """Runs preprocessing steps before the optional CacheDatasetPlaceholder."""
        if not self.supports_caching:
            return dataset
        with utils.map_seed_manager(seed):
            return self._preprocess_dataset(dataset, self._preprocessors[:self._cache_step_idx])

    def preprocess_postcache(self, dataset: tf.data.Dataset, sequence_length: Optional[Mapping[str, int]], seed: Optional[int]=None) -> tf.data.Dataset:
        """Runs preprocessing steps after the optional CacheDatasetPlaceholder.

    Args:
      dataset: a tf.data.Dataset
      sequence_length: dict mapping feature key to int length for that feature.
        If None, the features will not be truncated.
      seed: an optional random seed for deterministic preprocessing.

    Returns:
      a tf.data.Dataset
    """
        start_idx = 0
        if self.supports_caching:
            seed = None if seed is None else seed + 42 * self._cache_step_idx
            start_idx = self._cache_step_idx + 1
        with utils.map_seed_manager(seed):
            dataset = self._preprocess_dataset(dataset, self._preprocessors[start_idx:], sequence_length=sequence_length)
        return dataset

    @property
    def cache_dir(self) -> Optional[str]:
        """Returns the cache directory (or None), initializing if needed."""
        if not self._cache_dir:
            potential_cache_dirs = [os.path.join(d, utils.get_task_dir_from_name(self.name)) for d in utils.get_global_cache_dirs()]
            for cache_dir in potential_cache_dirs:
                try:
                    if tf.io.gfile.exists(os.path.join(cache_dir, 'COMPLETED')):
                        self._cache_dir = cache_dir
                        logging.info("'%s' is cached at %s.", self.name, self.cache_dir)
                        break
                except tf.errors.PermissionDeniedError:
                    logging.warning('Permission denied for global cache folder: %s', cache_dir)
                except tf.errors.FailedPreconditionError as e:
                    logging.warning('Failed precondition for global cache folder: %s with %r', cache_dir, e)
            if not self._cache_dir:
                logging.info("'%s' does not exist in any task cache directories (searched %s).", self.name, potential_cache_dirs)
        logging.info("Using cache directory %s for '%s'.", self._cache_dir, self.name)
        return self._cache_dir

    @property
    def supports_caching(self) -> bool:
        """Whether or not this task supports offline caching."""
        return self._cache_step_idx is not None

    @property
    def requires_caching(self) -> bool:
        """Whether or not this task requires offline caching."""
        return self._cache_step_idx is not None and self.preprocessors[self._cache_step_idx].required

    def assert_cached(self) -> None:
        """Raises an assertion error if cached dataset does not exist."""
        assert self.cache_dir, f"'{self.name}' does not exist in any of the task cache directories."

    def get_cached_stats(self, split: str=tfds.Split.TRAIN) -> Mapping[str, Union[int, float]]:
        """Returns basic statistics for cached dataset."""
        self.assert_cached()
        if split not in self._stats:
            stats_path = utils.get_cached_stats_path(self.cache_dir, split)
            if not tf.io.gfile.exists(stats_path):
                raise ValueError("Stats do not exist for '%s' split: %s" % (self.name, split))
            with tf.io.gfile.GFile(stats_path) as f:
                self._stats[split] = json.load(f)
        return self._stats[split]

    def get_dataset(self, sequence_length: Optional[Mapping[str, int]], split: str=tfds.Split.TRAIN, use_cached: bool=False, shuffle: bool=True, shuffle_buffer_size: Optional[int]=None, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None, num_epochs: Optional[int]=1, trim_output_features: bool=True) -> tf.data.Dataset:
        """Returns a tf.data.Dataset from cache or generated on the fly.

    Args:
      sequence_length: dict mapping feature key to maximum int length for that
        feature. If longer after preprocessing, the feature will be truncated.
        May be set to None to avoid truncation.
      split: string, the split to return.
      use_cached: bool, whether to use the cached dataset instead of processing
        it on the fly. Defaults to False.
      shuffle: bool, whether to shuffle the dataset. Only used when generating
        on the fly (use_cached=False).
      shuffle_buffer_size: an integer or None to use task-specific buffer size.
      seed: tf.int64 scalar tf.Tensor (or None) for shuffling tf.data.
      shard_info: optional specification for loading a shard of the split. If
        the Task's DataSource contains at least the number of shards in the
        specification, it will be passed the shard info to avoid loading the
        full source dataset. Otherwise, the full source dataset will be loaded
        and sharded at the individual examples.
      num_epochs: the number of times to iterate through the dataset, or `None`
        to repeat indefinitely. Note that the repeat occurs in the pipeline
        after offline caching, but before applying potentially stochastic
        post-cache preprocessors and is therefore typically preferred to calling
        `repeat()` on the returned dataset. Defaults to `1`.
        trim_output_features: If True, it trims output features to be less than
        the length given by `sequence_length`.

    Returns:
      A tf.data.Dataset.
    """
        if use_cached and (not self.supports_caching):
            logging.warning("Task '%s' does not support caching. Switching to on-the-fly preprocessing.", self.name)
            use_cached = False
        elif self.requires_caching and (not use_cached):
            raise ValueError(f"Task '{self.name}' requires caching, but was called with `use_cached=False`.")
        if use_cached:
            file_shuffle_buffer_size = self.preprocessors[self._cache_step_idx].file_shuffle_buffer_size
            source = self._get_cached_source(split, file_shuffle_buffer_size)
        else:
            source = self.source
        if source.supports_arbitrary_sharding:
            shard_data_source = True
        elif shard_info:
            shard_data_source = len(self.source.list_shards(split=split)) >= shard_info.num_shards
            logging.info('Sharding at the %s: %d of %d', 'data source' if shard_data_source else 'examples', shard_info.index, shard_info.num_shards)
        else:
            shard_data_source = False
            shard_info = ShardInfo(0, 1)
        if shard_data_source:
            ds = source.get_dataset(split=split, shuffle=shuffle, seed=seed, shard_info=shard_info)
        else:
            ds = source.get_dataset(split=split, shuffle=shuffle, seed=seed)
            ds = ds.shard(shard_info.num_shards, shard_info.index)
        if use_cached and self.get_cached_stats(split)['examples'] < _MAX_EXAMPLES_TO_MEM_CACHE or (self.num_input_examples(split) and self.num_input_examples(split) < _MAX_EXAMPLES_TO_MEM_CACHE):
            logging.info("Automatically caching small dataset in memory: '%s:%s'", self.name, split)
            ds = ds.cache()
        if not use_cached:
            ds = self.preprocess_precache(ds, seed=seed)
        ds = ds.prefetch(tf.data.experimental.AUTOTUNE)
        ds = ds.repeat(num_epochs)
        ds = self.preprocess_postcache(ds, sequence_length=sequence_length, seed=seed)
        ds = self._validate_preprocessing(ds)
        if trim_output_features:
            ds = self._trim_output_features(ds, sequence_length=sequence_length)
        if shuffle:
            if self._shuffle_buffer_size is None:
                raise ValueError(f"Shuffling is disallowed for Task '{self.name}' since its `shuffle_buffer_size` was set to `None` on construction.")
            shuffle_buffer_size = shuffle_buffer_size or self._shuffle_buffer_size
            ds = ds.shuffle(shuffle_buffer_size, seed=seed)
        return ds.prefetch(tf.data.experimental.AUTOTUNE)

    def _get_cached_source(self, split, file_shuffle_buffer_size: Optional[int]=None) -> _CachedDataSource:
        """Returns a DataSource to read cached files for split."""
        self.assert_cached()
        return _CachedDataSource(self.cache_dir, split, file_shuffle_buffer_size=file_shuffle_buffer_size)

    def postprocess_fn(self, decoded_model_output: Any, **postprocess_kwargs) -> Any:
        """Returns the model output after applying the postprocess function."""
        if self._postprocess_fn:
            return self._postprocess_fn(decoded_model_output, **postprocess_kwargs)
        return decoded_model_output

class TaskRegistry(DatasetProviderRegistry):
    """Registry of Tasks."""
    _REGISTRY = {}
    _PROVIDER_TYPE = Task

    @classmethod
    def add(cls, name: str, source: DataSourceInterface, output_features: Mapping[str, Feature], preprocessors: Optional[Sequence[Callable[..., tf.data.Dataset]]]=None, postprocess_fn: Optional[Callable[..., Any]]=None, metric_fns: Optional[Sequence[MetricFnCallable]]=None, metric_objs: Optional[Sequence[clu.metrics.Metric]]=None, task_cls: Type[Task]=Task, **kwargs) -> Task:
        """See `Task` constructor for docstring."""
        provider_kwargs = {'name': name, 'source': source, 'output_features': output_features, 'preprocessors': preprocessors, 'postprocess_fn': postprocess_fn, 'metric_fns': metric_fns, 'metric_objs': metric_objs, **kwargs}
        return super().add(name, provider_cls=task_cls, provider_kwargs=provider_kwargs)

    @classmethod
    def get(cls, name) -> Task:
        return super().get(name)
SampleFn = Callable[[Sequence[tf.data.Dataset], Sequence[float], Optional[int]], tf.data.Dataset]

class Mixture(DatasetProviderBase):
    """Class for mixing multiple tasks."""

    def __init__(self, name: str, tasks: Union[Sequence[str], Sequence[Tuple[str, Union[int, float, Callable[[Task], float]]]]], default_rate: Optional[Union[float, Callable[[Task], float]]]=None, sample_fn: SampleFn=tf.data.experimental.sample_from_datasets):
        """Mixture constructor.

    A mixture specifies a set of tasks with associated mixing rates.

    Mixing happens on preprocessed tokenized examples.

    The mixing rates represent relative numbers of examples to use from their
    associated tasks.  Setting the mixing rates to be equal to the numbers of
    examples in the tasks will result in each task going through an epoch in
    about the same amount of time - i.e. all examples are sampled equally across
    all tasks.

    Rates can be expressed either as absolute numbers or as functions that
    receive the Task as an argument.

    Args:
      name: string, a unique name for the Mixture.
      tasks: a list where each element is either a string (task name) or a pair
        whose first element is the task name and whose second element is either
        a float (rate) or a function from Task to float.
      default_rate: a float or a function from Task to float. This specifies the
        default rate if rates are not provided in the `tasks` argument.
      sample_fn: SampleFn callable that implements sampling logic to interleave
        multiple datasets into a single dataset.
    """
        self._task_to_rate = {}
        self._tasks = []
        self._sub_mixtures = []
        self._name = name
        self._sample_fn = sample_fn
        for t in tasks:
            if isinstance(t, str):
                task_name = t
                rate = default_rate
                if default_rate is None:
                    raise ValueError('need a rate for each task')
            else:
                task_name, rate = t
            if task_name in TaskRegistry.names():
                self._tasks.append(TaskRegistry.get(task_name))
                self._task_to_rate[task_name] = rate
            else:
                self._sub_mixtures.append(MixtureRegistry.get(task_name))
                self._task_to_rate[task_name] = rate
        if len(set((tuple(t.output_features) for t in self.tasks))) != 1:
            raise ValueError('All Tasks in a Mixture must have the same output features.')

    @property
    def name(self) -> str:
        return self._name

    @property
    def tasks(self) -> Sequence[Task]:
        sub_tasks = (mix.tasks for mix in self._sub_mixtures)
        return list(sorted(set(sum(sub_tasks, self._tasks)), key=lambda t: t.name))

    @property
    def total_rate(self) -> float:
        return sum((float(rate(TaskRegistry.get(name)) if callable(rate) else rate) for name, rate in self._task_to_rate.items()))

    def get_rate(self, task: Task) -> float:
        """Computes the mixing rate for the given task."""
        value = 0.0
        for mix in self._sub_mixtures:
            if task in mix.tasks:
                rate = self._task_to_rate[mix.name]
                value += rate * mix.get_rate(task) / mix.total_rate
        if task.name in self._task_to_rate:
            rate = self._task_to_rate[task.name]
            value += float(rate(task) if callable(rate) else rate)
        return value

    def num_input_examples(self, split: str) -> int:
        return sum((t.num_input_examples(split) for t in self.tasks))

    @property
    def splits(self) -> Sequence[str]:
        splits = set()
        for task in self.tasks:
            splits.update(task.splits)
        return tuple(splits)

    @property
    def output_features(self) -> Mapping[str, Feature]:
        return self.tasks[0].output_features

    def _check_compatible_features(self) -> None:
        """Throw Exception if features across tasks have different vocabs or dtypes."""
        for name, feature in self.tasks[0].output_features.items():
            for task in self.tasks[1:]:
                if hasattr(feature, 'vocabulary') and task.output_features[name].vocabulary != feature.vocabulary:
                    raise ValueError('Features across tasks in a mixture must use the same vocabulary.')
                if task.output_features[name].dtype != feature.dtype:
                    raise ValueError('Features across tasks in a mixture must use the same dtype.')

    def get_dataset(self, sequence_length: Optional[Mapping[str, int]], split: str=tfds.Split.TRAIN, use_cached: bool=False, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None, num_epochs: Optional[int]=None, copy_pretokenized: bool=False, compute_stats_empirically: bool=False, log_mixing_proportions: bool=True, passthrough_features: Optional[Sequence[str]]=None, trim_output_features: bool=True) -> tf.data.Dataset:
        """Returns the dataset of mixed tasks using the object-specified rates.

    Args:
      sequence_length: dict mapping feature key to maximum int length for that
        feature. If longer after preprocessing, the feature will be truncated.
        May be set to None to avoid truncation.
      split: string, the split to return for all tasks.
      use_cached: bool, whether to use the cached dataset instead of processing
        it on the fly. Defaults to False.
      shuffle: bool, whether to shuffle the dataset.  Only used when generating
        on the fly (use_cached=False).
      seed: tf.int64 scalar tf.Tensor (or None) for shuffling tf.data.
      shard_info: optional specification for loading a shard of the split.
      num_epochs: the number of times to iterate through the dataset, or `None`
        to repeat indefinitely. Note that the repeat occurs in the pipeline
        after offline caching, but before applying potentially stochastic
        post-cache preprocessors and is therefore typically preferred to calling
        `repeat()` on the returned dataset. Defaults to `None`.
      copy_pretokenized: bool, whether to pass through copies of pretokenized
        features a "_pretokenized" suffix added to the key.
      compute_stats_empirically: a boolean - does not work on TPU
      log_mixing_proportions: whether to log the mixing porportions of the tasks
      passthrough_features: a list of additional features that will be kept
        after the feature filtering. If set to be None, then only the
        output_features defined for the mixture will be kept.
      trim_output_features: If True, it trims output features to be less than
        the length given by `sequence_length`.
    """
        self._check_compatible_features()
        tasks = []
        for task in self.tasks:
            if split not in task.splits:
                logging.warning("Task %s has no '%s' split, skipping.", task.name, split)
                continue
            tasks.append(task)
        if not tasks:
            raise ValueError("No datasets have a '{}' split".format(split))
        output_feature_keys = set(self.output_features.keys())
        if copy_pretokenized:
            output_feature_keys.update({f + '_pretokenized' for f in output_feature_keys})
        if passthrough_features:
            output_feature_keys.update(passthrough_features)

        def filter_features(ex):
            return {k: v for k, v in ex.items() if k in output_feature_keys}
        datasets: List[tf.data.Dataset] = []
        for task in tasks:
            try:
                ds = task.get_dataset(sequence_length, split=split, use_cached=use_cached, shuffle=shuffle, seed=seed, shard_info=shard_info, num_epochs=num_epochs, trim_output_features=trim_output_features).map(filter_features, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                datasets.append(ds)
            except:
                logging.error("Failed to load task '%s' as part of mixture '%s'", task.name, self.name)
                raise
        rates = [self.get_rate(task) for task in tasks]
        if seed is not None:
            sample_seed = seed
        elif shuffle:
            sample_seed = None
        else:
            sample_seed = 42
        dataset = self._sample_fn(datasets, rates, sample_seed)
        if log_mixing_proportions and split == 'train' and use_cached and all((t.supports_caching for t in tasks)):
            _log_mixing_proportions(tasks, datasets, rates, dataset, sequence_length, compute_stats_empirically)
        return dataset

def _log_padding_fractions(dataset, sequence_length, num_examples=100):
    """Empirically compute the fraction of padding - log the results.

  Args:
    dataset: a tf.data.Dataset
    sequence_length: dict from string to int (packed lengths)
    num_examples: an integer
  """
    logging.info('computing padding fractions')
    keys = sequence_length.keys()
    padding_frac = {k: 0 for k in keys}
    for ex in tfds.as_numpy(dataset.take(num_examples)):
        for k in keys:
            padding_frac[k] += 1 - sequence_length[k] / len(ex[k])
    for k in keys:
        logging.info('%s padding fraction = %g', k, padding_frac[k])

def _log_mixing_proportions(tasks, datasets, rates, mixed_dataset, sequence_length, compute_stats_empirically):
    """Log information about the mixing proportions.

  Called from Mixture.get_dataset.

  Args:
    tasks: a list of Task
    datasets: a list of tf.data.Dataset
    rates: a list of floats
    mixed_dataset: a tf.data.Dataset
    sequence_length: dict from string to int (packed lengths)
    compute_stats_empirically: a boolean - does not work on TPU
  """

    def _normalize(l):
        denom = sum(l)
        if not denom:
            return l
        return [x / denom for x in l]
    examples_fraction = _normalize(rates)
    if compute_stats_empirically:
        stats_examples = 100
        mean_inputs_length = []
        mean_targets_length = []
        for dataset in datasets:
            inputs_sum = 0
            targets_sum = 0
            for ex in tfds.as_numpy(dataset.take(stats_examples)):
                if 'inputs' in ex:
                    inputs_sum += ex['inputs'].size
                targets_sum += ex['targets'].size
            mean_inputs_length.append(inputs_sum / float(stats_examples))
            mean_targets_length.append(targets_sum / float(stats_examples))
    else:

        def _estimated_mean_length(task, key):
            if key not in sequence_length:
                return 0
            if task.supports_caching and task._cache_step_idx < len(task._preprocessors) - 1:
                return sequence_length[key]
            if key + '_tokens' in task.get_cached_stats('train'):
                return min(sequence_length[key], task.get_cached_stats('train')[key + '_tokens'] / task.get_cached_stats('train')['examples'])
            else:
                return 0
        mean_inputs_length = [_estimated_mean_length(task, 'inputs') for task in tasks]
        mean_targets_length = [_estimated_mean_length(task, 'targets') for task in tasks]
    inputs_fraction = _normalize([l * r for l, r in zip(mean_inputs_length, rates)])
    targets_fraction = _normalize([l * r for l, r in zip(mean_targets_length, rates)])
    logging.info('%12s %12s %12s %12s %12s %12s %s', 'rate', 'ex.frac.', 'inp.frac.', 'tgt.frac.', 'inp.len.', 'tgt.len', 'task')
    for i in range(len(rates)):
        logging.info('%12g %12g %12g %12g %12g %12g %s', rates[i], examples_fraction[i], inputs_fraction[i], targets_fraction[i], mean_inputs_length[i], mean_targets_length[i], tasks[i].name)
    if compute_stats_empirically:
        _log_padding_fractions(mixed_dataset, sequence_length)

class MixtureRegistry(DatasetProviderRegistry):
    """Registry of Mixtures."""
    _REGISTRY = {}
    _PROVIDER_TYPE = Mixture

    @classmethod
    def add(cls, name, tasks, default_rate=None, mixture_cls: Type[Mixture]=Mixture, **kwargs) -> Mixture:
        """See `Mixture` constructor for docstring."""
        provider_kwargs = {'name': name, 'tasks': tasks, 'default_rate': default_rate, **kwargs}
        return super().add(name, provider_cls=mixture_cls, provider_kwargs=provider_kwargs)

    @classmethod
    def get(cls, name) -> Mixture:
        return super().get(name)

def get_mixture_or_task(task_or_mixture_name):
    """Return the Task or Mixture from the appropriate registry."""
    mixtures = MixtureRegistry.names()
    tasks = TaskRegistry.names()
    if task_or_mixture_name in mixtures:
        if task_or_mixture_name in tasks:
            logging.warning('%s is both a Task and a Mixture, returning Mixture', task_or_mixture_name)
        return MixtureRegistry.get(task_or_mixture_name)
    if task_or_mixture_name in tasks:
        return TaskRegistry.get(task_or_mixture_name)
    else:
        for available_task in sorted(tasks):
            logging.info('Available task: %s', available_task)
        for available_mixture in sorted(mixtures):
            logging.info('Available mixture: %s', available_mixture)
        raise ValueError("No Task or Mixture found with name '%s'." % task_or_mixture_name)

def get_subtasks(task_or_mixture):
    """Returns all the Tasks in a Mixture as a list or the Task itself."""
    if isinstance(task_or_mixture, Task):
        return [task_or_mixture]
    else:
        return task_or_mixture.tasks

def get_dataset(mixture_or_task_name: str, task_feature_lengths: Mapping[str, int], feature_converter: FeatureConverter, dataset_split: str='train', use_cached: bool=False, shuffle: bool=False, num_epochs: Optional[int]=1, shard_info: Optional[ShardInfo]=None, verbose: bool=True, seed: Optional[int]=None, batch_size: Optional[int]=None, trim_output_features: bool=True) -> tf.data.Dataset:
    """Get processed dataset with the model features.

  In order to use options specific to a feature converter, e.g., packing,
  `feature_converter` instance should be instantiated with those options before
  being pased to this function.

  Getting sharded datasets is supported. To use this feature, pass in
  `shard_info`, with shard_index and num_shards information. Sharding is done
  before the feature converter stage. Therefore, if packing is used it will be
  done on the sharded dataset.

  Args:
    mixture_or_task_name: mixture or task name for the Task API.
    task_feature_lengths: dict mapping task feature key to its sequence length.
      This specifies the sequence length of the dataset from the Task API.
    feature_converter: a feature converter object to use to convert the task
      features to model features. Must be a subclass of FeatureConverter.
    dataset_split: the split to use.
    use_cached: whether to use the cached dataset instead of processing it on
      the fly.
    shuffle: whether to shuffle the dataset.
    num_epochs: the number of times to iterate through the dataset, or `None` to
      repeat indefinitely. Note that the repeat occurs in the pipeline after
      offline caching, but before applying potentially stochastic post-cache
      preprocessors and is therefore typically preferred to calling `repeat()`
      on the returned dataset. Defaults to `1`.
    shard_info: number of shards and shard index information.
    verbose: if true, log the feature shapes.
    seed: a random seed to for shuffling tf.data.
    batch_size: Optional batch size.
    trim_output_features: If True, it trims output features to be less than the
      length given by `sequence_length`.

  Returns:
    ds: the processed dataset.
  """
    if not isinstance(feature_converter, FeatureConverter):
        raise TypeError('feature_converter should be an instance of FeatureConverter.')
    mixture_or_task = get_mixture_or_task(mixture_or_task_name)
    is_grain_task = False
    if is_grain_task:
        ds = mixture_or_task.get_dataset(sequence_length=task_feature_lengths, split=dataset_split, use_cached=use_cached, shuffle=shuffle, seed=seed, shard_info=shard_info, num_epochs=num_epochs, batch_size=batch_size, feature_converter=feature_converter, trim_output_features=trim_output_features)
    else:
        ds = mixture_or_task.get_dataset(task_feature_lengths, split=dataset_split, use_cached=use_cached, shuffle=shuffle, seed=seed, shard_info=shard_info, num_epochs=num_epochs, trim_output_features=trim_output_features)
        ds = feature_converter(ds, task_feature_lengths=task_feature_lengths)
        if batch_size is not None:
            ds = ds.batch(batch_size, drop_remainder=True)
    if verbose:
        logging.info('The output dataset from seqio.get_dataset has the following features')
        element_spec = utils.flatten_dict(ds.element_spec, delimiter='.')
        for feature_name, tensor_spec in element_spec.items():
            if isinstance(tensor_spec, tf.TensorSpec):
                logging.info('feature: %s \t shape: %s \t dtype: %s', feature_name, tensor_spec.shape.as_list(), tensor_spec.dtype.name)
            else:
                logging.error('Unknown tensor_spec type %s for feature %s.', type(tensor_spec), feature_name)
    return ds