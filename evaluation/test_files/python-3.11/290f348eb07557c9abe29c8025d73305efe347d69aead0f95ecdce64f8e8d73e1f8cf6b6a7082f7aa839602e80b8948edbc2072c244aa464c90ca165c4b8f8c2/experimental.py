"""Experimental utilities for SeqIO."""
import functools
import inspect
from typing import Callable, Iterable, Mapping, Optional, Sequence
from absl import logging
from seqio import dataset_providers
from seqio import preprocessors as seqio_preprocessors
from seqio import utils
import tensorflow as tf
import tensorflow_datasets as tfds
CacheDatasetPlaceholder = dataset_providers.CacheDatasetPlaceholder
Mixture = dataset_providers.Mixture
MixtureRegistry = dataset_providers.MixtureRegistry
ShardInfo = dataset_providers.ShardInfo
Task = dataset_providers.Task
TaskRegistry = dataset_providers.TaskRegistry

def _get_fully_cached_name(original_name: str, sequence_length: Mapping[str, int]) -> str:
    """Generates name for fully-cached task or mixture."""
    new_name = f'{original_name}_'
    prefix_len = 0
    while len(set((feat[:prefix_len] for feat in sequence_length))) != len(sequence_length):
        prefix_len += 1
    new_name += '_'.join((f'{feat[:prefix_len]}{sequence_length[feat]}' for feat in sequence_length))
    return new_name

def add_fully_cached_task(task_name: str, sequence_length: Mapping[str, int], disallow_shuffling: bool=False) -> Task:
    """Adds fully-cached version of the task for given sequence lengths."""
    task = TaskRegistry.get(task_name)
    new_name = _get_fully_cached_name(task_name, sequence_length)
    try:
        return TaskRegistry.get(new_name)
    except ValueError:
        pass
    fixed_sequence_length = sequence_length
    new_preprocessors = []
    for prep in task.preprocessors:
        if isinstance(prep, CacheDatasetPlaceholder):
            continue

        def wrapped_prep(ds, output_features, prep=prep):
            prep_args = inspect.signature(prep).parameters.keys()
            extra_kwargs = {}
            if 'sequence_length' in prep_args:
                extra_kwargs['sequence_length'] = fixed_sequence_length
            if 'output_features' in prep_args:
                extra_kwargs['output_features'] = output_features
            return prep(ds, **extra_kwargs)
        new_preprocessors.append(wrapped_prep)
    new_preprocessors.append(CacheDatasetPlaceholder(required=True))

    def validate_sequence_length(ds, sequence_length):
        if sequence_length is not None and dict(sequence_length) != dict(fixed_sequence_length):
            raise ValueError(f"Fully-cached task '{new_name}' can only be loaded with `sequence_length={fixed_sequence_length}` or `None`. Given sequence_length={sequence_length}.")
        return ds
    new_preprocessors.append(validate_sequence_length)
    logging.info("Registering fully cached Task '%s' with sequence lengths %s.", new_name, sequence_length)
    return TaskRegistry.add(new_name, source=task.source, preprocessors=new_preprocessors, output_features=task.output_features, metric_fns=task.metric_fns, postprocess_fn=task.postprocessor, shuffle_buffer_size=None if disallow_shuffling else dataset_providers.SHUFFLE_BUFFER_SIZE)

def add_fully_cached_mixture(mixture_name: str, sequence_length: Mapping[str, int], disallow_shuffling: bool=False) -> Mixture:
    """Adds fully-cached version of the mixture for given sequence lengths."""
    mixture = MixtureRegistry.get(mixture_name)
    new_name = _get_fully_cached_name(mixture_name, sequence_length)
    new_tasks = [add_fully_cached_task(task.name, sequence_length, disallow_shuffling) for task in mixture.tasks]
    logging.info("Registering fully cached Mixture '%s' with sequence lengths %s.", new_name, sequence_length)
    return MixtureRegistry.add(new_name, [(new_t.name, mixture._task_to_rate[old_t.name]) for old_t, new_t in zip(mixture.tasks, new_tasks)])

class FewshotDataSource(dataset_providers.DataSource):
    """Combines two splits of another `DataSource` to provide fewshot examples.

  Output examples are a dictionary containing a single eval example and a batch
  of train examples. For example, with `num_shots=2`:

  {
    'train': {
        'inputs': [
            'How many Beatles are there?', 'How many Beatles are alive in 2020?'
        ],
        'targets': ['4', '2']
    },
    'eval': {
        'inputs': 'What city were the Beatles from?'
        'targets': 'Liverpool'
    }
  }

  Note that if `num_shots` is 0, the 'train' entry will not be included in the
  resulting examples.
  """

    def __init__(self, original_source: dataset_providers.DataSource, num_shots: int, train_preprocessors: Iterable[Callable[[tf.data.Dataset], tf.data.Dataset]]=(), eval_preprocessors: Iterable[Callable[[tf.data.Dataset], tf.data.Dataset]]=(), train_split: str='train', train_feature_keys: Iterable[str]=('inputs', 'targets'), shuffle_buffer_size: int=dataset_providers.SHUFFLE_BUFFER_SIZE, eval_on_fixed_exemplars: bool=False):
        """Initializes FewshotDataSource.

    Args:
      original_source: a DataSource to produce fewshot examples from.
      num_shots: A non-negative integer specifying how many training examples to
        include in the inputs.
      train_preprocessors: an iterable of preprocessors to run on the train
        split before zipping with the eval split.
      eval_preprocessors: an iterable of preprocessors to run on the eval split
        before zipping with the train split.
      train_split: the split to use as training examples.
      train_feature_keys: the features to retain in the train split after
        preprocessing but before batching zipping with the eval split. This is
        necessary to remove variable-length sequences, which cannot be batched.
      shuffle_buffer_size: size of the shuffle buffer used when calling
        `get_dataset` with shuffle=True. Note that separate shuffles are applied
        to the `train` and `eval` splits before they are combined.
      eval_on_fixed_exemplars: If True, uses a fixed set of exemplars at
        evaluation time. Only effective during evaluation when `split` not
        equals `self._train_split`.
    """
        self._original_source = original_source
        self._num_shots = num_shots
        self._train_preprocessors = train_preprocessors
        self._eval_preprocessors = eval_preprocessors
        self._train_split = train_split
        self._train_feature_keys = train_feature_keys
        self._shuffle_buffer_size = shuffle_buffer_size
        self._eval_on_fixed_exemplars = eval_on_fixed_exemplars
        super().__init__(splits=())

    @property
    def splits(self) -> Sequence[str]:
        return self._original_source.splits

    @property
    def supports_arbitrary_sharding(self) -> bool:
        return False

    def list_shards(self, split: str) -> Sequence[str]:
        return self._original_source.list_shards(split)

    def get_dataset(self, split: str=tfds.Split.TRAIN, shuffle: bool=True, seed: Optional[int]=None, shard_info: Optional[ShardInfo]=None, *, sequence_length: Optional[Mapping[str, int]]=None, use_cached: bool=False, num_epochs: Optional[int]=1) -> tf.data.Dataset:
        shard_info: ShardInfo = shard_info or ShardInfo(0, 1)
        if self._train_split not in self._original_source.splits:
            raise ValueError(f"Train split '{self._train_split}' is not one of the original source splits: {self._original_source.splits}")
        if not self._num_shots:
            logging.warning('Train examples will not be included in the provided dataset since `num_shots` is 0.')

        def _apply_preprocessors(ds, preprocessors):
            for prep_fn in preprocessors:
                ds = prep_fn(ds)
            return ds

        def _get_maybe_sharded_dataset(split_: str, shuffle_: bool, seed_: int) -> tf.data.Dataset:
            """Shard at source if possible, but fall back to examples if not."""
            num_shards = len(self._original_source.list_shards(split_))
            if num_shards >= shard_info.num_shards:
                ds = self._original_source.get_dataset(split=split_, shuffle=shuffle_, seed=seed_, shard_info=shard_info)
            else:
                ds = self._original_source.get_dataset(split=split_, shuffle=shuffle_, seed=seed_).shard(shard_info.num_shards, shard_info.index)
            if shuffle_:
                ds = ds.shuffle(buffer_size=self._shuffle_buffer_size, seed=seed_, reshuffle_each_iteration=True)
            return ds
        if seed is None:
            train_seed = None
            eval_seed = None
        else:
            train_seed = seed
            eval_seed = seed + 1
        datasets = {}
        if self._num_shots:
            train_ds = _get_maybe_sharded_dataset(split_=self._train_split, shuffle_=True, seed_=train_seed if shuffle else 0)
            train_ds = _apply_preprocessors(train_ds, self._train_preprocessors)
            train_ds = train_ds.map(lambda x: {k: x[k] for k in self._train_feature_keys}, num_parallel_calls=tf.data.experimental.AUTOTUNE)
            train_ds = train_ds.repeat().batch(self._num_shots)
            if self._eval_on_fixed_exemplars and split != self._train_split:
                train_ds = train_ds.take(1).cache().repeat()
            datasets['train'] = train_ds
        eval_ds = _get_maybe_sharded_dataset(split_=split, shuffle_=shuffle, seed_=eval_seed)
        eval_ds = _apply_preprocessors(eval_ds, self._eval_preprocessors)
        datasets['eval'] = eval_ds
        return tf.data.Dataset.zip(datasets)

def fewshot_preprocessor(ds, inputs_prefix='', targets_prefix='', example_separator='\n\n', prompt='', reverse=False):
    """Create 'inputs' and 'targets' strings for (zero/few)-shot evaluation.

  Inputs and targets will be formatted using the given prefixes along with a
  separator between each pair. The few-shot examples from the train set will
  include both inputs and targets, whereas the eval example (at the end) will
  contain only the input followed by the targets prefix.

  NOTE: The final target prefix will be right-stripped so that the input does
  not end with whitepsace.

  For example, a 2-shot output might look like:
  output: {
    'inputs':
      '0 How many states in the US? X 1 50 X 0 How many cents in a dollar? X '
      '1 100 X 0 Who was in the Beatles? X 1',
    'targets': 'John',
    'answers': ['John', 'Paul', 'George', 'Ringo']
  }

  Args:
    ds: A dictionary of zipped eval and train tf.data.Datasets, each
      preprocessed with at least the fields 'inputs' and 'targets'. Note that
      the train dataset will not exist in the 0-shot case.
    inputs_prefix: Prefix string for inputs.
    targets_prefix: Prefix string for targets.
    example_separator: The string separator to delimit different examples.
    prompt: Optional prefix for the entire few-shot input. Typically consists of
      a natural language description of the task or task instructions.
    reverse: If True, the list of few shot examples is reversed. If used with
      eval_on_fixed_exemplars = True and a fixed train_seed, the last N shots
      will be the same when num_shots is N or N+M. In other words, additional
      shots are prepended instead of appended.

  Returns:
    A tf.data.Dataset containing 'inputs', 'targets', and any other features
    from the evaluation dataset.
  """

    @utils.map_over_dataset
    def fewshot_map(ex):
        if 'train' in ex:
            train_examples = tf.stack([inputs_prefix + ex['train']['inputs'], targets_prefix + ex['train']['targets'] + example_separator], axis=1)
            if reverse:
                train_examples = tf.reverse(train_examples, [0])
            shots = tf.strings.reduce_join(tf.reshape(train_examples, [-1]))
        else:
            shots = ''
        if prompt:
            shots = tf.strings.join([prompt, shots], separator=example_separator)
        new_ex = {'inputs': shots + inputs_prefix + ex['eval']['inputs'] + targets_prefix.rstrip(), 'targets': ex['eval']['targets']}
        new_ex.update({k: v for k, v in ex['eval'].items() if k not in ('inputs', 'targets')})
        return new_ex
    ds = fewshot_map(ds)
    if ds.element_spec['inputs'].shape.rank:
        ds = ds.unbatch()
    return ds

def add_task_with_sentinels(task_name: str, num_sentinels: Optional[int]=1):
    """Adds sentinels to the inputs/outputs of a task.

  Adds num_sentinels sentinels to the end of 'inputs' and at the beginning
  of 'targets'. This is known to help fine-tuning span corruption models,
  especially on smaller datasets.

  This will also rename the task by adding a "_{num_sentinels}_sentinel" suffix
  to the task name, but making sure it comes before the following suffixes:
  '_train', '_dev', '_test', '.'.

  Example before:
  'inputs': What is the captial of illinois?
  'targets': Springfield.

  Example after:
  'inputs': What is the captial of illinois? <extra_id_0>
  'targets': <extra_id_0> Springfield.

  Args:
    task_name: a str, which is the name of the task you want to have sentinels
      added to. Note this will not override the current task, but will create a
      new one.
    num_sentinels: integer, number of sentinels to end of inputs and the
      beginning of targets.
  """

    def _append_eos_after_trim_and_preserve(dataset: tf.data.Dataset, output_features: Mapping[str, dataset_providers.Feature], sequence_length: Optional[Mapping[str, int]]=None, preserve_final_n_tokens_when_trimming: Optional[int]=None) -> tf.data.Dataset:
        """Version of append_eos_after_trim with option to preserve last n tokens."""

        def _maybe_add_eos_and_trim(key: str, value: tf.Tensor) -> tf.Tensor:
            if key not in output_features or not output_features[key].add_eos:
                return value
            eos_id = output_features[key].vocabulary.eos_id
            if sequence_length is not None and sequence_length.get(key, None) is not None:
                max_length = sequence_length[key]
                if preserve_final_n_tokens_when_trimming is not None and preserve_final_n_tokens_when_trimming > 0:
                    trimmed_length = tf.minimum(max_length, tf.shape(value)[0] + 1)
                    n_tokens_to_preserve = tf.minimum(preserve_final_n_tokens_when_trimming, trimmed_length - 1)
                    return tf.concat([value[:trimmed_length - (n_tokens_to_preserve + 1)], value[-n_tokens_to_preserve:], [eos_id]], axis=0)
                else:
                    return tf.concat([value[:max_length - 1], [eos_id]], axis=0)
            else:
                return tf.concat([value, [eos_id]], axis=0)
        return dataset.map(lambda ex: {k: _maybe_add_eos_and_trim(k, v) for k, v in ex.items()}, num_parallel_calls=tf.data.experimental.AUTOTUNE)

    def _create_new_task_name(task_name):
        """Creates the new task name with sentinels added."""
        sentinel_name = '_{}_sentinel'.format(num_sentinels)
        for suffix in ['_train', '_dev', '_test', '_eval', '.']:
            idx = task_name.find(suffix)
            if idx >= 0:
                return task_name[:idx] + sentinel_name + task_name[idx:]
        return task_name + sentinel_name

    def _sentinel_id(vocabulary, sentinel_num=0):
        """Token ID to use as a sentinel.

    Args:
      vocabulary: a t5.data.vocabularies.Vocabulary
      sentinel_num: an optional interger, what sentinel should be returned. By
        default it returns the first sentinel.

    Returns:
      an integer
    """
        return vocabulary.vocab_size - 1 - sentinel_num

    def _add_sentinels(dataset, sequence_length, output_features):
        """Adds sentinels to end of inputs and beginning of targets."""
        del sequence_length
        input_vocab = output_features['inputs'].vocabulary
        target_vocab = output_features['targets'].vocabulary

        @utils.map_over_dataset
        def _my_fn(x):
            sentinels_input = [_sentinel_id(input_vocab, idx) for idx in range(num_sentinels)]
            sentinels_output = [_sentinel_id(target_vocab, idx) for idx in range(num_sentinels)]
            x['inputs'] = tf.concat([x['inputs'], sentinels_input], 0)
            x['targets'] = tf.concat([sentinels_output, x['targets']], 0)
            return x
        return _my_fn(dataset)

    def _postprocess_fn_remove_sentinel(string_label, *args, **kwargs):
        """If sentinels are appended to the task, then remove them before eval."""
        del args
        del kwargs
        vocab = task.output_features['targets'].vocabulary
        sentinel_str = vocab.decode([_sentinel_id(vocab, idx) for idx in range(num_sentinels)])
        if string_label.startswith(sentinel_str):
            string_label = string_label[len(sentinel_str):].strip()
        return string_label

    def _wrap_postprocess_fn_remove_sentinel(postprocess_fn):
        """Wrap around another postprocess_fn to remove sentinels first."""

        def new_fn(string_label, *args, **kwargs):
            string_label = _postprocess_fn_remove_sentinel(string_label, *args, **kwargs)
            return postprocess_fn(string_label, *args, **kwargs)
        return new_fn
    task = TaskRegistry.get(task_name)
    sentinel_task_name = _create_new_task_name(task_name)
    new_preprocessors = list(task.preprocessors)
    if new_preprocessors[-1] is seqio_preprocessors.append_eos_after_trim:
        new_eos_funtion = functools.partial(_append_eos_after_trim_and_preserve, preserve_final_n_tokens_when_trimming=num_sentinels)
        new_preprocessors[-1] = new_eos_funtion
        new_preprocessors.insert(-1, _add_sentinels)
    else:
        new_preprocessors.append(_add_sentinels)
    postprocess_fn = task.postprocessor
    if postprocess_fn is not None:
        new_postprocess_fn = _wrap_postprocess_fn_remove_sentinel(postprocess_fn)
    else:
        new_postprocess_fn = _postprocess_fn_remove_sentinel
    TaskRegistry.add(sentinel_task_name, source=task.source, preprocessors=new_preprocessors, output_features=task.output_features, postprocess_fn=new_postprocess_fn, metric_fns=task.metric_fns)