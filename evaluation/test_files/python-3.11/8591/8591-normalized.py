def _read_result(self):
    """Parse read a response from the AGI and parse it.

        :return dict: The AGI response parsed into a dict.
        """
    response = (yield from self.reader.readline())
    return parse_agi_result(response.decode(self.encoding)[:-1])