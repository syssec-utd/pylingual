def load_systemjs_manifest(self):
    """
        Load the existing systemjs manifest and remove any entries that no longer
        exist on the storage.
        """
    _manifest_name = self.manifest_name
    self.manifest_name = self.systemjs_manifest_name
    bundle_files = self.load_manifest()
    self.manifest_name = _manifest_name
    for file, hashed_file in bundle_files.copy().items():
        if not self.exists(file) or not self.exists(hashed_file):
            del bundle_files[file]
    return bundle_files