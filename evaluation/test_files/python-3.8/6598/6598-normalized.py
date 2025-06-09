def put(self, item):
    """Put an item into the queue. Items should be comparable, eg. tuples.
        True - if item placed in queue.
        False - if queue is full and item can not be placed."""
    if self.__maxsize and len(self.__data) >= self.__maxsize:
        return False
    heapq.heappush(self.__data, item)
    return True