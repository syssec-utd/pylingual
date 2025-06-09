def load(cls, filename):
    """ Load a pickled Dataset instance from file. """
    try:
        dataset = pickle.load(open(filename, 'rb'))
    except UnicodeDecodeError:
        dataset = pickle.load(open(filename, 'rb'), encoding='latin')
    if hasattr(dataset, 'feature_table'):
        dataset.feature_table._csr_to_sdf()
    return dataset