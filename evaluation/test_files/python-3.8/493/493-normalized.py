def get_file_to_stream(self, stream, share_name, directory_name, file_name, **kwargs):
    """
        Download a file from Azure File Share.

        :param stream: A filehandle to store the file to.
        :type stream: file-like object
        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.get_file_to_stream()` takes.
        :type kwargs: object
        """
    self.connection.get_file_to_stream(share_name, directory_name, file_name, stream, **kwargs)