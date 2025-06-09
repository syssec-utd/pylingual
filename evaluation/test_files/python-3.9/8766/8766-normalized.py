def clean_old_index(model, block_size=100, **kwargs):
    """
    This utility function will clean out old index data that was accidentally
    left during item deletion in rom versions <= 0.27.0 . You should run this
    after you have upgraded all of your clients to version 0.28.0 or later.

    Arguments:

        * *model* - the model whose entities you want to reindex
        * *block_size* - the maximum number of items to check at a time
          defaulting to 100

    This function will yield its progression through re-checking all of the
    data that could be left over.

    Example use::

        for progress, total in clean_old_index(MyModel, block_size=200):
            print "%s of %s"%(progress, total)
    """
    conn = _connect(model)
    version = list(map(int, conn.info()['redis_version'].split('.')[:2]))
    has_hscan = version >= [2, 8]
    pipe = conn.pipeline(True)
    prefix = '%s:' % model._namespace
    index = prefix + ':'
    block_size = max(block_size, 10)
    force_hscan = kwargs.get('force_hscan', False)
    if (has_hscan or force_hscan) and force_hscan is not None:
        max_id = conn.hlen(index)
        cursor = None
        scanned = 0
        while cursor != b'0':
            (cursor, remove) = _scan_index_lua(conn, [index, prefix], [cursor or '0', block_size, 0, 0])
            if remove:
                _clean_index_lua(conn, [model._namespace], remove)
            scanned += block_size
            if scanned > max_id:
                max_id = scanned + 1
            yield (scanned, max_id)
        for uniq in chain(model._unique, model._cunique):
            name = uniq if isinstance(uniq, six.string_types) else ':'.join(uniq)
            idx = prefix + name + ':uidx'
            cursor = None
            while cursor != b'0':
                (cursor, remove) = _scan_index_lua(conn, [idx, prefix], [cursor or '0', block_size, 1, 0])
                if remove:
                    conn.hdel(idx, *remove)
                scanned += block_size
                if scanned > max_id:
                    max_id = scanned + 1
                yield (scanned, max_id)
    else:
        if model._unique or model._cunique:
            if has_hscan:
                warnings.warn('You have disabled the use of HSCAN to clean up indexes, this will prevent unique index cleanup', stacklevel=2)
            else:
                warnings.warn('Unique indexes cannot be cleaned up in Redis versions prior to 2.8', stacklevel=2)
        max_id = int(conn.get('%s%s:' % (prefix, model._pkey)) or '0')
        for i in range(1, max_id + 1, block_size):
            ids = list(range(i, min(i + block_size, max_id + 1)))
            for id in ids:
                pipe.exists(prefix + str(id))
                pipe.hexists(index, id)
            result = iter(pipe.execute())
            remove = [id for (id, ent, ind) in zip(ids, result, result) if ind and (not ent)]
            if remove:
                _clean_index_lua(conn, [model._namespace], remove)
            yield (min(i + block_size, max_id - 1), max_id)
    yield (max_id, max_id)