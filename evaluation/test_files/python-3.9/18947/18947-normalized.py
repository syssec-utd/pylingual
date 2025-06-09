def static(self, root, path, media_type=None, charset='UTF-8'):
    """Send content of a static file as response.

        The path to the document root directory should be specified as
        the root argument. This is very important to prevent directory
        traversal attack. This method guarantees that only files within
        the document root directory are served and no files outside this
        directory can be accessed by a client.

        The path to the actual file to be returned should be specified
        as the path argument. This path must be relative to the document
        directory.

        The *media_type* and *charset* arguments are used to set the
        Content-Type header of the HTTP response. If *media_type*
        is not specified or specified as ``None`` (the default), then it
        is guessed from the filename of the file to be returned.

        Arguments:
          root (str): Path to document root directory.
          path (str): Path to file relative to document root directory.
          media_type (str, optional): Media type of file.
          charset (str, optional): Character set of file.

        Returns:
          bytes: Content of file to be returned in the HTTP response.
        """
    root = os.path.abspath(os.path.join(root, ''))
    path = os.path.abspath(os.path.join(root, path.lstrip('/\\')))
    self.response.state['filename'] = os.path.basename(path)
    if not path.startswith(root):
        return 403
    elif not os.path.isfile(path):
        return 404
    if media_type is not None:
        self.response.media_type = media_type
    else:
        self.response.media_type = mimetypes.guess_type(path)[0]
    self.response.charset = charset
    with open(path, 'rb') as f:
        return f.read()