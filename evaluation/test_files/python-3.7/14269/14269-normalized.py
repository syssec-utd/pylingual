def add_secondary_linked_file(self, file_path, relpath=None, mimetype=None, time_origin=None, assoc_with=None):
    """Add a secondary linked file.

        :param str file_path: Path of the file.
        :param str relpath: Relative path of the file.
        :param str mimetype: Mimetype of the file, if ``None`` it tries to
            guess it according to the file extension which currently only works
            for wav, mpg, mpeg and xml.
        :param int time_origin: Time origin for the media file.
        :param str assoc_with: Associated with field.
        :raises KeyError: If mimetype had to be guessed and a non standard
                          extension or an unknown mimetype.
        """
    if mimetype is None:
        mimetype = self.MIMES[file_path.split('.')[-1]]
    self.linked_file_descriptors.append({'LINK_URL': file_path, 'RELATIVE_LINK_URL': relpath, 'MIME_TYPE': mimetype, 'TIME_ORIGIN': time_origin, 'ASSOCIATED_WITH': assoc_with})