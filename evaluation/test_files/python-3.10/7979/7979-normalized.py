def _warn_if_not_at_expected_pos(self, expected_pos, end_of, start_of):
    """ Helper function to warn about unknown bytes found in the file"""
    diff = expected_pos - self.stream.tell()
    if diff != 0:
        logger.warning('There are {} bytes between {} and {}'.format(diff, end_of, start_of))