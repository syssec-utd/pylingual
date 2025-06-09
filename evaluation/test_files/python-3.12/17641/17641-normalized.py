def get_generator(self, path, *args, **kw_args):
    """
        Get a generator that allows convenient access to the streamed data.
        Elements from the dataset are returned from the generator one row at a time.
        Unlike the direct access queue, this generator also returns the remainder elements.
        Additional arguments are forwarded to get_queue.
        See the get_queue method for documentation of these parameters.

        :param path:
        :return: A generator that iterates over the rows in the dataset.
        """
    q = self.get_queue(*args, path=path, **kw_args)
    try:
        for guard in q.iter():
            with guard as batch:
                batch_copy = batch.copy()
            for row in batch_copy:
                yield row
        last_batch = self.get_remainder(path, q.block_size)
        for row in last_batch:
            yield row
    finally:
        q.close()