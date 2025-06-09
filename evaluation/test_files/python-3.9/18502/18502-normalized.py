def _delete_s3(self, filename, bucket_name):
    """Deletes the specified file from the given S3 bucket."""
    conn = S3Connection(self.access_key_id, self.access_key_secret)
    bucket = conn.get_bucket(bucket_name)
    if type(filename).__name__ == 'Key':
        filename = '/' + filename.name
    path = self._get_s3_path(filename)
    k = Key(bucket)
    k.key = path
    try:
        bucket.delete_key(k)
    except S3ResponseError:
        pass