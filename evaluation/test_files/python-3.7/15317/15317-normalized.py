def caffe_to_tensorflow_session(caffe_def_path, caffemodel_path, inputs, graph_name='Graph', conversion_out_dir_path=None, use_padding_same=False):
    """Create a TensorFlow Session from a Caffe model."""
    try:
        from caffeflow import convert
    except ImportError:
        raise Exception('caffeflow package needs to be installed to freeze Caffe models. Check out the README file.')
    with dummy_context_mgr(conversion_out_dir_path) or util.TemporaryDirectory() as dir_path:
        params_values_output_path = os.path.join(dir_path, 'params_values.npy')
        network_output_path = os.path.join(dir_path, 'network.py')
        convert.convert(caffe_def_path, caffemodel_path, params_values_output_path, network_output_path, False, use_padding_same=use_padding_same)
        network_module = imp.load_source('module.name', network_output_path)
        network_class = getattr(network_module, graph_name)
        network = network_class(inputs)
        sess = tf.Session()
        network.load(params_values_output_path, sess)
        return sess