def fill_parameters(self, path, blocks, exclude_free_params=False, check_parameters=False):
    """
        Load parameters from file to fill all blocks sequentially.
        :type blocks: list of deepy.layers.Block
        """
    if not os.path.exists(path):
        raise Exception('model {} does not exist'.format(path))
    normal_params = sum([nn.parameters for nn in blocks], [])
    all_params = sum([nn.all_parameters for nn in blocks], [])
    if path.endswith('.gz'):
        opener = gzip.open if path.lower().endswith('.gz') else open
        handle = opener(path, 'rb')
        saved_params = pickle.load(handle)
        handle.close()
        if len(all_params) != len(saved_params):
            logging.warning('parameters in the network: {}, parameters in the dumped model: {}'.format(len(all_params), len(saved_params)))
        for (target, source) in zip(all_params, saved_params):
            if not exclude_free_params or target not in normal_params:
                target.set_value(source)
    elif path.endswith('.npz'):
        arrs = np.load(path)
        if len(all_params) != len(arrs.keys()):
            logging.warning('parameters in the network: {}, parameters in the dumped model: {}'.format(len(all_params), len(arrs.keys())))
        for (target, idx) in zip(all_params, range(len(arrs.keys()))):
            if not exclude_free_params or target not in normal_params:
                source = arrs['arr_%d' % idx]
                target.set_value(source)
    else:
        raise Exception("File format of %s is not supported, use '.gz' or '.npz' or '.uncompressed.gz'" % path)