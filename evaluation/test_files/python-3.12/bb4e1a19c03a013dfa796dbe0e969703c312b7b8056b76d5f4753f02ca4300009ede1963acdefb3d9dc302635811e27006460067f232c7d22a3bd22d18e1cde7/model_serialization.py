"""Classes and functions implementing to Model SavedModel serialization."""
from keras.saving import saving_utils
from keras.saving.saved_model import constants
from keras.saving.saved_model import layer_serialization
from keras.saving.saved_model import save_impl

class ModelSavedModelSaver(layer_serialization.LayerSavedModelSaver):
    """Model SavedModel serialization."""

    @property
    def object_identifier(self):
        return constants.MODEL_IDENTIFIER

    def _python_properties_internal(self):
        metadata = super()._python_properties_internal()
        metadata.pop('stateful')
        metadata['is_graph_network'] = self.obj._is_graph_network
        spec = self.obj.save_spec(dynamic_batch=False)
        metadata['full_save_spec'] = spec
        metadata['save_spec'] = None if spec is None else spec[0][0]
        metadata.update(saving_utils.model_metadata(self.obj, include_optimizer=True, require_config=False))
        return metadata

    def _get_serialized_attributes_internal(self, serialization_cache):
        default_signature = None
        if len(serialization_cache[constants.KERAS_CACHE_KEY]) == 1:
            default_signature = save_impl.default_save_signature(self.obj)
        objects, functions = super()._get_serialized_attributes_internal(serialization_cache)
        functions['_default_save_signature'] = default_signature
        return (objects, functions)

class SequentialSavedModelSaver(ModelSavedModelSaver):

    @property
    def object_identifier(self):
        return constants.SEQUENTIAL_IDENTIFIER