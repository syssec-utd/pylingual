def load_keras(json_path=None, hdf5_path=None, by_name=False):
    """
        Load a pre-trained Keras model.

        :param json_path: The json path containing the keras model definition.
        :param hdf5_path: The HDF5 path containing the pre-trained keras model weights with or without the model architecture.
        :return: A bigdl model.
        """
    import os
    try:
        import tensorflow
    except ImportError:
        os.environ['KERAS_BACKEND'] = 'theano'
        try:
            from theano import ifelse
        except ImportError:
            raise Exception('No backend is found for Keras. Please install either tensorflow or theano.')
    from bigdl.keras.converter import DefinitionLoader, WeightLoader
    if json_path and (not hdf5_path):
        return DefinitionLoader.from_json_path(json_path)
    elif json_path and hdf5_path:
        return WeightLoader.load_weights_from_json_hdf5(json_path, hdf5_path, by_name=by_name)
    elif hdf5_path and (not json_path):
        (kmodel, bmodel) = DefinitionLoader.from_hdf5_path(hdf5_path)
        WeightLoader.load_weights_from_kmodel(bmodel, kmodel)
        return bmodel