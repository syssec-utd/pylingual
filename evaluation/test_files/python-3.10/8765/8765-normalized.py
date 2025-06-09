def refresh_indices(model, block_size=100):
    """
    This utility function will iterate over all entities of a provided model,
    refreshing their indices. This is primarily useful after adding an index
    on a column.

    Arguments:

        * *model* - the model whose entities you want to reindex
        * *block_size* - the maximum number of entities you want to fetch from
          Redis at a time, defaulting to 100

    This function will yield its progression through re-indexing all of your
    entities.

    Example use::

        for progress, total in refresh_indices(MyModel, block_size=200):
            print "%s of %s"%(progress, total)

    .. note:: This uses the session object to handle index refresh via calls to
      ``.commit()``. If you have any outstanding entities known in the
      session, they will be committed.
    """
    conn = _connect(model)
    max_id = int(conn.get('%s:%s:' % (model._namespace, model._pkey)) or '0')
    block_size = max(block_size, 10)
    for i in range(1, max_id + 1, block_size):
        models = model.get(list(range(i, i + block_size)))
        models
        session.commit(all=True)
        yield (min(i + block_size, max_id), max_id)