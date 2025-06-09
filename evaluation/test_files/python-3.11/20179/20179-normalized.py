def mergesort(list_of_lists, key=None):
    """ Perform an N-way merge operation on sorted lists.

    @param list_of_lists: (really iterable of iterable) of sorted elements
    (either by naturally or by C{key})
    @param key: specify sort key function (like C{sort()}, C{sorted()})

    Yields tuples of the form C{(item, iterator)}, where the iterator is the
    built-in list iterator or something you pass in, if you pre-generate the
    iterators.

    This is a stable merge; complexity O(N lg N)

    Examples::

    >>> print list(mergesort([[1,2,3,4],
    ...                      [2,3.25,3.75,4.5,6,7],
    ...                      [2.625,3.625,6.625,9]]))
    [1, 2, 2, 2.625, 3, 3.25, 3.625, 3.75, 4, 4.5, 6, 6.625, 7, 9]

    # note stability
    >>> print list(mergesort([[1,2,3,4],
    ...                      [2,3.25,3.75,4.5,6,7],
    ...                      [2.625,3.625,6.625,9]],
    ...                      key=int))
    [1, 2, 2, 2.625, 3, 3.25, 3.75, 3.625, 4, 4.5, 6, 6.625, 7, 9]


    >>> print list(mergesort([[4, 3, 2, 1],
    ...                      [7, 6, 4.5, 3.75, 3.25, 2],
    ...                      [9, 6.625, 3.625, 2.625]],
    ...                      key=lambda x: -x))
    [9, 7, 6.625, 6, 4.5, 4, 3.75, 3.625, 3.25, 3, 2.625, 2, 2, 1]
    """
    heap = []
    for i, itr in enumerate((iter(pl) for pl in list_of_lists)):
        try:
            item = itr.next()
            if key:
                toadd = (key(item), i, item, itr)
            else:
                toadd = (item, i, itr)
            heap.append(toadd)
        except StopIteration:
            pass
    heapq.heapify(heap)
    if key:
        while heap:
            _, idx, item, itr = heap[0]
            yield item
            try:
                item = itr.next()
                heapq.heapreplace(heap, (key(item), idx, item, itr))
            except StopIteration:
                heapq.heappop(heap)
    else:
        while heap:
            item, idx, itr = heap[0]
            yield item
            try:
                heapq.heapreplace(heap, (itr.next(), idx, itr))
            except StopIteration:
                heapq.heappop(heap)