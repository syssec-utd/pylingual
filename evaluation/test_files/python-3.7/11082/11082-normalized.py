def add(self, *args):
    """
        Add one or more files or URLs to the manifest.
        If files contains a glob, it is expanded.

        All files are uploaded to SolveBio. The Upload
        object is used to fill the manifest.
        """

    def _is_url(path):
        p = urlparse(path)
        return bool(p.scheme)
    for path in args:
        path = os.path.expanduser(path)
        if _is_url(path):
            self.add_url(path)
        elif os.path.isfile(path):
            self.add_file(path)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                self.add_file(f)
        elif glob.glob(path):
            for f in glob.glob(path):
                self.add_file(f)
        else:
            raise ValueError('Path: "{0}" is not a valid format or does not exist. Manifest paths must be files, directories, or URLs.'.format(path))