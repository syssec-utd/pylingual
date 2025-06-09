def copy_object(self, source_bucket_key, dest_bucket_key, source_bucket_name=None, dest_bucket_name=None, source_version_id=None):
    """
        Creates a copy of an object that is already stored in S3.

        Note: the S3 connection used here needs to have access to both
        source and destination bucket/key.

        :param source_bucket_key: The key of the source object.

            It can be either full s3:// style url or relative path from root level.

            When it's specified as a full s3:// url, please omit source_bucket_name.
        :type source_bucket_key: str
        :param dest_bucket_key: The key of the object to copy to.

            The convention to specify `dest_bucket_key` is the same
            as `source_bucket_key`.
        :type dest_bucket_key: str
        :param source_bucket_name: Name of the S3 bucket where the source object is in.

            It should be omitted when `source_bucket_key` is provided as a full s3:// url.
        :type source_bucket_name: str
        :param dest_bucket_name: Name of the S3 bucket to where the object is copied.

            It should be omitted when `dest_bucket_key` is provided as a full s3:// url.
        :type dest_bucket_name: str
        :param source_version_id: Version ID of the source object (OPTIONAL)
        :type source_version_id: str
        """
    if dest_bucket_name is None:
        (dest_bucket_name, dest_bucket_key) = self.parse_s3_url(dest_bucket_key)
    else:
        parsed_url = urlparse(dest_bucket_key)
        if parsed_url.scheme != '' or parsed_url.netloc != '':
            raise AirflowException('If dest_bucket_name is provided, ' + 'dest_bucket_key should be relative path ' + 'from root level, rather than a full s3:// url')
    if source_bucket_name is None:
        (source_bucket_name, source_bucket_key) = self.parse_s3_url(source_bucket_key)
    else:
        parsed_url = urlparse(source_bucket_key)
        if parsed_url.scheme != '' or parsed_url.netloc != '':
            raise AirflowException('If source_bucket_name is provided, ' + 'source_bucket_key should be relative path ' + 'from root level, rather than a full s3:// url')
    CopySource = {'Bucket': source_bucket_name, 'Key': source_bucket_key, 'VersionId': source_version_id}
    response = self.get_conn().copy_object(Bucket=dest_bucket_name, Key=dest_bucket_key, CopySource=CopySource)
    return response