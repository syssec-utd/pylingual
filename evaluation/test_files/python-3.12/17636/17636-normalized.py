def get_direct(self):
    """
        Allows direct access to the buffer element.
        Blocks until there is data that can be read.

        :return: A guard object that returns the buffer element.
        """
    read_idx = self.__get_idx()
    if read_idx is QueueClosed:
        return QueueClosed
    return self.Guard(self.write_queue, self.arys, lambda: read_idx)