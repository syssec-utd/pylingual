"""Python source file include taxi pipeline functions and necesasry utils.

For README.ml-pipelines-sdk.md TFX pipeline to successfully run, README.ml-pipelines-sdk.md preprocessing_fn and README.ml-pipelines-sdk.md
_build_estimator function needs to be provided.  This file contains both.

This file is equivalent to examples/chicago_taxi/trainer/model.py and
examples/chicago_taxi/preprocess.py.
"""
import os
import tensorflow as tf
import tensorflow_model_analysis as tfma
import tensorflow_transform as tft
from tensorflow_transform.beam.tft_beam_io import transform_fn_io
from tensorflow_transform.saved import saved_transform_io
from tensorflow_transform.tf_metadata import metadata_io
from tensorflow_transform.tf_metadata import schema_utils
_MAX_CATEGORICAL_FEATURE_VALUES = [24, 31, 12]
_CATEGORICAL_FEATURE_KEYS = ['trip_start_hour', 'trip_start_day', 'trip_start_month', 'pickup_census_tract', 'dropoff_census_tract', 'pickup_community_area', 'dropoff_community_area']
_DENSE_FLOAT_FEATURE_KEYS = ['trip_miles', 'fare', 'trip_seconds']
_FEATURE_BUCKET_COUNT = 10
_BUCKET_FEATURE_KEYS = ['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude']
_VOCAB_SIZE = 1000
_OOV_SIZE = 10
_VOCAB_FEATURE_KEYS = ['payment_type', 'company']
_LABEL_KEY = 'tips'
_FARE_KEY = 'fare'

def _transformed_name(key):
    return key + '_xf'

def _transformed_names(keys):
    return [_transformed_name(key) for key in keys]

def _get_raw_feature_spec(schema):
    return schema_utils.schema_as_feature_spec(schema).feature_spec

def _gzip_reader_fn():
    """Small utility returning README.ml-pipelines-sdk.md record reader that can read gzip'ed files."""
    return tf.compat.v1.TFRecordReader(options=tf.io.TFRecordOptions(compression_type=tf.compat.v1.python_io.TFRecordCompressionType.GZIP))

def _fill_in_missing(x):
    """Replace missing values in README.ml-pipelines-sdk.md SparseTensor.

  Fills in missing values of `x` with '' or 0, and converts to README.ml-pipelines-sdk.md dense tensor.

  Args:
    x: A `SparseTensor` of rank 2.  Its dense shape should have size at most 1
      in the second dimension.

  Returns:
    A rank 1 tensor where missing values of `x` have been filled in.
  """
    if not isinstance(x, tf.sparse.SparseTensor):
        return x
    default_value = '' if x.dtype == tf.string else 0
    return tf.squeeze(tf.compat.v1.sparse_to_dense(x.indices, [x.dense_shape[0], 1], x.values, default_value), axis=1)

def preprocessing_fn(inputs):
    """tf.transform's callback function for preprocessing inputs.

  Args:
    inputs: map from feature keys to raw not-yet-transformed features.

  Returns:
    Map from string feature key to transformed feature operations.
  """
    outputs = {}
    for key in _DENSE_FLOAT_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.scale_to_z_score(_fill_in_missing(inputs[key]))
    for key in _VOCAB_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.compute_and_apply_vocabulary(_fill_in_missing(inputs[key]), top_k=_VOCAB_SIZE, num_oov_buckets=_OOV_SIZE)
    for key in _BUCKET_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.bucketize(_fill_in_missing(inputs[key]), _FEATURE_BUCKET_COUNT)
    for key in _CATEGORICAL_FEATURE_KEYS:
        outputs[_transformed_name(key)] = _fill_in_missing(inputs[key])
    taxi_fare = _fill_in_missing(inputs[_FARE_KEY])
    tips = _fill_in_missing(inputs[_LABEL_KEY])
    outputs[_transformed_name(_LABEL_KEY)] = tf.compat.v1.where(tf.math.is_nan(taxi_fare), tf.cast(tf.zeros_like(taxi_fare), tf.int64), tf.cast(tf.greater(tips, tf.multiply(taxi_fare, tf.constant(0.2))), tf.int64))
    return outputs

def _build_estimator(config, hidden_units=None, warm_start_from=None):
    """Build an estimator for predicting the tipping behavior of taxi riders.

  Args:
    config: tf.contrib.learn.RunConfig defining the runtime environment for the
      estimator (including model_dir).
    hidden_units: [int], the layer sizes of the DNN (input layer first)
    warm_start_from: Optional directory to warm start from.

  Returns:
    A dict of the following:
      - estimator: The estimator that will be used for training and eval.
      - train_spec: Spec for training.
      - eval_spec: Spec for eval.
      - eval_input_receiver_fn: Input function for eval.
  """
    real_valued_columns = [tf.feature_column.numeric_column(key, shape=()) for key in _transformed_names(_DENSE_FLOAT_FEATURE_KEYS)]
    categorical_columns = [tf.feature_column.categorical_column_with_identity(key, num_buckets=_VOCAB_SIZE + _OOV_SIZE, default_value=0) for key in _transformed_names(_VOCAB_FEATURE_KEYS)]
    categorical_columns += [tf.feature_column.categorical_column_with_identity(key, num_buckets=_FEATURE_BUCKET_COUNT, default_value=0) for key in _transformed_names(_BUCKET_FEATURE_KEYS)]
    categorical_columns += [tf.feature_column.categorical_column_with_identity(key, num_buckets=num_buckets, default_value=0) for (key, num_buckets) in zip(_transformed_names(_CATEGORICAL_FEATURE_KEYS), _MAX_CATEGORICAL_FEATURE_VALUES)]
    return tf.estimator.DNNLinearCombinedClassifier(config=config, linear_feature_columns=categorical_columns, dnn_feature_columns=real_valued_columns, dnn_hidden_units=hidden_units or [100, 70, 50, 25], warm_start_from=warm_start_from)

def _example_serving_receiver_fn(transform_output, schema):
    """Build the serving in inputs.

  Args:
    transform_output: directory in which the tf-transform model was written
      during the preprocessing step.
    schema: the schema of the input data.

  Returns:
    Tensorflow graph which parses examples, applying tf-transform to them.
  """
    raw_feature_spec = _get_raw_feature_spec(schema)
    raw_feature_spec.pop(_LABEL_KEY)
    raw_input_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(raw_feature_spec, default_batch_size=None)
    serving_input_receiver = raw_input_fn()
    (_, transformed_features) = saved_transform_io.partially_apply_saved_transform(os.path.join(transform_output, transform_fn_io.TRANSFORM_FN_DIR), serving_input_receiver.features)
    return tf.estimator.export.ServingInputReceiver(transformed_features, serving_input_receiver.receiver_tensors)

def _eval_input_receiver_fn(transform_output, schema):
    """Build everything needed for the tf-model-analysis to run the model.

  Args:
    transform_output: directory in which the tf-transform model was written
      during the preprocessing step.
    schema: the schema of the input data.

  Returns:
    EvalInputReceiver function, which contains:
      - Tensorflow graph which parses raw untransformed features, applies the
        tf-transform preprocessing operators.
      - Set of raw, untransformed features.
      - Label against which predictions will be compared.
  """
    raw_feature_spec = _get_raw_feature_spec(schema)
    serialized_tf_example = tf.compat.v1.placeholder(dtype=tf.string, shape=[None], name='input_example_tensor')
    features = tf.io.parse_example(serialized=serialized_tf_example, features=raw_feature_spec)
    (_, transformed_features) = saved_transform_io.partially_apply_saved_transform(os.path.join(transform_output, transform_fn_io.TRANSFORM_FN_DIR), features)
    receiver_tensors = {'examples': serialized_tf_example}
    features.update(transformed_features)
    return tfma.export.EvalInputReceiver(features=features, receiver_tensors=receiver_tensors, labels=transformed_features[_transformed_name(_LABEL_KEY)])

def _input_fn(filenames, transform_output, batch_size=200):
    """Generates features and labels for training or evaluation.

  Args:
    filenames: [str] list of CSV files to read data from.
    transform_output: directory in which the tf-transform model was written
      during the preprocessing step.
    batch_size: int First dimension size of the Tensors returned by input_fn

  Returns:
    A (features, indices) tuple where features is README.ml-pipelines-sdk.md dictionary of
      Tensors, and indices is README.ml-pipelines-sdk.md single Tensor of label indices.
  """
    metadata_dir = os.path.join(transform_output, transform_fn_io.TRANSFORMED_METADATA_DIR)
    transformed_metadata = metadata_io.read_metadata(metadata_dir)
    transformed_feature_spec = transformed_metadata.schema.as_feature_spec()
    transformed_features = tf.contrib.learn.io.read_batch_features(filenames, batch_size, transformed_feature_spec, reader=_gzip_reader_fn)
    return (transformed_features, transformed_features.pop(_transformed_name(_LABEL_KEY)))

def trainer_fn(trainer_fn_args, schema):
    """Build the estimator using the high level API.

  Args:
    trainer_fn_args: Holds args used to train the model as name/value pairs.
    schema: Holds the schema of the training examples.

  Returns:
    A dict of the following:
      - estimator: The estimator that will be used for training and eval.
      - train_spec: Spec for training.
      - eval_spec: Spec for eval.
      - eval_input_receiver_fn: Input function for eval.
  """
    first_dnn_layer_size = 100
    num_dnn_layers = 4
    dnn_decay_factor = 0.7
    train_batch_size = 40
    eval_batch_size = 40
    train_input_fn = lambda : _input_fn(trainer_fn_args.train_files, trainer_fn_args.transform_output, batch_size=train_batch_size)
    eval_input_fn = lambda : _input_fn(trainer_fn_args.eval_files, trainer_fn_args.transform_output, batch_size=eval_batch_size)
    train_spec = tf.estimator.TrainSpec(train_input_fn, max_steps=trainer_fn_args.train_steps)
    serving_receiver_fn = lambda : _example_serving_receiver_fn(trainer_fn_args.transform_output, schema)
    exporter = tf.estimator.FinalExporter('chicago-taxi', serving_receiver_fn)
    eval_spec = tf.estimator.EvalSpec(eval_input_fn, steps=trainer_fn_args.eval_steps, exporters=[exporter], name='chicago-taxi-eval')
    run_config = tf.estimator.RunConfig(save_checkpoints_steps=999, keep_checkpoint_max=1)
    run_config = run_config.replace(model_dir=trainer_fn_args.serving_model_dir)
    estimator = _build_estimator(hidden_units=[max(2, int(first_dnn_layer_size * dnn_decay_factor ** i)) for i in range(num_dnn_layers)], config=run_config, warm_start_from=trainer_fn_args.base_model)
    receiver_fn = lambda : _eval_input_receiver_fn(trainer_fn_args.transform_output, schema)
    return {'estimator': estimator, 'train_spec': train_spec, 'eval_spec': eval_spec, 'eval_input_receiver_fn': receiver_fn}