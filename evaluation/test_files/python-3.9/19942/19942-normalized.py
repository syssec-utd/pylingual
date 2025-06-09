def define_index(self, idx_name, create, transform):
    """Add an index to this store instance.

        Adds an index transform to the current FC store. Once an index
        with name ``idx_name`` is added, it will be available in all
        ``index_*`` methods. Additionally, the index will be automatically
        updated on calls to :meth:`~dossier.fc.store.Store.put`.

        If an index with name ``idx_name`` already exists, then it is
        overwritten.

        Note that indexes do *not* persist. They must be re-defined for
        each instance of :class:`Store`.

        For example, to add an index on the ``boNAME`` feature, you can
        use the ``feature_index`` helper function:

        .. code-block:: python

            store.define_index('boNAME',
                               feature_index('boNAME'),
                               lambda s: s.encode('utf-8'))

        Another example for creating an index on names:

        .. code-block:: python

            store.define_index('NAME',
                               feature_index('canonical_name', 'NAME'),
                               lambda s: s.lower().encode('utf-8'))

        :param idx_name: The name of the index. Must be UTF-8 encodable.
        :type idx_name: unicode
        :param create: A function that accepts the ``transform`` function and
                       a pair of ``(content_id, fc)`` and produces a generator
                       of index values from the pair given using ``transform``.
        :param transform: A function that accepts an arbitrary value and
                          applies a transform to it. This transforms the
                          *stored* value to the *index* value. This *must*
                          produce a value with type `str` (or `bytes`).
        """
    assert isinstance(idx_name, (str, unicode))
    idx_name = idx_name.decode('utf-8')
    self._indexes[idx_name] = {'create': create, 'transform': transform}