def _unpack_by_int(self, data, current_position):
    """Returns a tuple with (location of next data field, contents of requested data field)."""
    try:
        requested_data_length = struct.unpack('>I', data[current_position:current_position + self.INT_LEN])[0]
    except struct.error:
        raise MalformedDataError('Unable to unpack %s bytes from the data' % self.INT_LEN)
    current_position += self.INT_LEN
    remaining_data_length = len(data[current_position:])
    if remaining_data_length < requested_data_length:
        raise MalformedDataError('Requested %s bytes, but only %s bytes available.' % (requested_data_length, remaining_data_length))
    next_data = data[current_position:current_position + requested_data_length]
    current_position += requested_data_length
    return (current_position, next_data)