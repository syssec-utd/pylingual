def network_from_pandas_hdf5(cls, filename):
    """
    Build a Network from data in a Pandas HDFStore.

    Parameters
    ----------
    cls : class
        Class to instantiate, usually pandana.Network.
    filename : str

    Returns
    -------
    network : pandana.Network

    """
    with pd.HDFStore(filename) as store:
        nodes = store['nodes']
        edges = store['edges']
        two_way = store['two_way'][0]
        imp_names = store['impedance_names'].tolist()
    return cls(nodes['x'], nodes['y'], edges['from'], edges['to'], edges[imp_names], twoway=two_way)