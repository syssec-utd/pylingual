def _initialize_archive(self):
    """Initialize archive based on the parsed parameters"""
    if 'archive_path' not in self.parsed_args:
        manager = None
    elif self.parsed_args.no_archive:
        manager = None
    else:
        if not self.parsed_args.archive_path:
            archive_path = os.path.expanduser(ARCHIVES_DEFAULT_PATH)
        else:
            archive_path = self.parsed_args.archive_path
        manager = ArchiveManager(archive_path)
    self.archive_manager = manager