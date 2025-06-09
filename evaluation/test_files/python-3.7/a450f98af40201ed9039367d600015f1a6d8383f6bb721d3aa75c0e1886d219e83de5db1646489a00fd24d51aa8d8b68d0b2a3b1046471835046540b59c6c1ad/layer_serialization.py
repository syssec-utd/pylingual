"""Classes and functions implementing Layer SavedModel serialization."""
import tensorflow.compat.v2 as tf
from keras.mixed_precision import policy
from keras.saving.legacy.saved_model import base_serialization
from keras.saving.legacy.saved_model import constants
from keras.saving.legacy.saved_model import save_impl
from keras.saving.legacy.saved_model import serialized_attributes
from keras.utils import generic_utils

class LayerSavedModelSaver(base_serialization.SavedModelSaver):
    """Implements Layer SavedModel serialization."""

    @property
    def object_identifier(self):
        return constants.LAYER_IDENTIFIER

    @property
    def python_properties(self):
        return self._python_properties_internal()

    def _python_properties_internal(self):
        """Returns dictionary of all python properties."""
        metadata = dict(name=self.obj.name, trainable=self.obj.trainable, expects_training_arg=self.obj._expects_training_arg, dtype=policy.serialize(self.obj._dtype_policy), batch_input_shape=getattr(self.obj, '_batch_input_shape', None), stateful=self.obj.stateful, must_restore_from_config=self.obj._must_restore_from_config, preserve_input_structure_in_config=self.obj._preserve_input_structure_in_config, autocast=self.obj._autocast)
        metadata.update(get_serialized(self.obj))
        if self.obj.input_spec is not None:
            metadata['input_spec'] = tf.nest.map_structure(lambda x: generic_utils.serialize_keras_object(x) if x else None, self.obj.input_spec)
        if self.obj.activity_regularizer is not None and hasattr(self.obj.activity_regularizer, 'get_config'):
            metadata['activity_regularizer'] = generic_utils.serialize_keras_object(self.obj.activity_regularizer)
        if self.obj._build_input_shape is not None:
            metadata['build_input_shape'] = self.obj._build_input_shape
        return metadata

    def objects_to_serialize(self, serialization_cache):
        return self._get_serialized_attributes(serialization_cache).objects_to_serialize

    def functions_to_serialize(self, serialization_cache):
        return self._get_serialized_attributes(serialization_cache).functions_to_serialize

    def _get_serialized_attributes(self, serialization_cache):
        """Generates or retrieves serialized attributes from cache."""
        keras_cache = serialization_cache.setdefault(constants.KERAS_CACHE_KEY, {})
        if self.obj in keras_cache:
            return keras_cache[self.obj]
        serialized_attr = keras_cache[self.obj] = serialized_attributes.SerializedAttributes.new(self.obj)
        if save_impl.should_skip_serialization(self.obj) or self.obj._must_restore_from_config:
            return serialized_attr
        (object_dict, function_dict) = self._get_serialized_attributes_internal(serialization_cache)
        serialized_attr.set_and_validate_objects(object_dict)
        serialized_attr.set_and_validate_functions(function_dict)
        return serialized_attr

    def _get_serialized_attributes_internal(self, serialization_cache):
        """Returns dictionary of serialized attributes."""
        objects = save_impl.wrap_layer_objects(self.obj, serialization_cache)
        functions = save_impl.wrap_layer_functions(self.obj, serialization_cache)
        functions['_default_save_signature'] = None
        return (objects, functions)

def get_serialized(obj):
    with generic_utils.skip_failed_serialization():
        return generic_utils.serialize_keras_object(obj)

class InputLayerSavedModelSaver(base_serialization.SavedModelSaver):
    """InputLayer serialization."""

    @property
    def object_identifier(self):
        return constants.INPUT_LAYER_IDENTIFIER

    @property
    def python_properties(self):
        return dict(class_name=type(self.obj).__name__, name=self.obj.name, dtype=self.obj.dtype, sparse=self.obj.sparse, ragged=self.obj.ragged, batch_input_shape=self.obj._batch_input_shape, config=self.obj.get_config())

    def objects_to_serialize(self, serialization_cache):
        return {}

    def functions_to_serialize(self, serialization_cache):
        return {}

class RNNSavedModelSaver(LayerSavedModelSaver):
    """RNN layer serialization."""

    @property
    def object_identifier(self):
        return constants.RNN_LAYER_IDENTIFIER

    def _get_serialized_attributes_internal(self, serialization_cache):
        (objects, functions) = super()._get_serialized_attributes_internal(serialization_cache)
        states = tf.__internal__.tracking.wrap(self.obj.states)
        if isinstance(states, tuple):
            states = tf.__internal__.tracking.wrap(list(states))
        objects['states'] = states
        return (objects, functions)

class VocabularySavedModelSaver(LayerSavedModelSaver):
    """Handles vocabulary layer serialization.

    This class is needed for StringLookup, IntegerLookup, and TextVectorization,
    which all have a vocabulary as part of the config. Currently, we keep this
    vocab as part of the config until saving, when we need to clear it to avoid
    initializing a StaticHashTable twice (once when restoring the config and
    once when restoring restoring module resources). After clearing the vocab,
    we persist a property to the layer indicating it was constructed with a
    vocab.
    """

    @property
    def python_properties(self):
        metadata = self._python_properties_internal()
        metadata['config']['vocabulary'] = None
        metadata['config']['has_input_vocabulary'] = self.obj._has_input_vocabulary
        return metadata