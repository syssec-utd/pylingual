def attach_file(self, locator_or_path, path=None, **kwargs):
    """
        Find a file field on the page and attach a file given its path. The file field can be found
        via its name, id, or label text. ::

            page.attach_file(locator, "/path/to/file.png")

        Args:
            locator_or_path (str): Which field to attach the file to, or the path of the file that
                will be attached.
            path (str, optional): The path of the file that will be attached. Defaults to
                ``locator_or_path``.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Raises:
            FileNotFound: No file exists at the given path.
        """
    if path is None:
        (locator, path) = (None, locator_or_path)
    else:
        locator = locator_or_path
    if not os.path.isfile(path):
        raise FileNotFound('cannot attach file, {0} does not exist'.format(path))
    self.find('file_field', locator, **kwargs).set(path)