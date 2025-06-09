def relative_filename(self, filename):
    """Return the relative form of `filename`.

        The filename will be relative to the current directory when the
        `FileLocator` was constructed.

        """
    fnorm = os.path.normcase(filename)
    if fnorm.startswith(self.relative_dir):
        filename = filename[len(self.relative_dir):]
    return filename