def prepare_files(self, finder):
    """
        Prepare process. Create temp directories, download and/or unpack files.
        """
    if self.wheel_download_dir:
        ensure_dir(self.wheel_download_dir)
    self._walk_req_to_install(functools.partial(self._prepare_file, finder))