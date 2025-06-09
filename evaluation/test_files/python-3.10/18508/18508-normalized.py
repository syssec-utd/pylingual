def find_by_path(self, path, storage_type=None, bucket_name=None):
    """Finds files at the specified path / prefix, either on S3 or on the local filesystem."""
    if not (storage_type and bucket_name):
        return self._find_by_path_local(path)
    else:
        if storage_type != 's3':
            raise ValueError('Storage type "%s" is invalid, the only supported storage type (apart from default local storage) is s3.' % storage_type)
        return self._find_by_path_s3(path, bucket_name)