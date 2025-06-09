def get_crc32c(self, bucket_name, object_name):
    """
        Gets the CRC32c checksum of an object in Google Cloud Storage.

        :param bucket_name: The Google cloud storage bucket where the blob_name is.
        :type bucket_name: str
        :param object_name: The name of the object to check in the Google cloud
            storage bucket_name.
        :type object_name: str
        """
    self.log.info('Retrieving the crc32c checksum of object_name: %s in bucket_name: %s', object_name, bucket_name)
    client = self.get_conn()
    bucket = client.get_bucket(bucket_name=bucket_name)
    blob = bucket.get_blob(blob_name=object_name)
    blob.reload()
    blob_crc32c = blob.crc32c
    self.log.info('The crc32c checksum of %s is %s', object_name, blob_crc32c)
    return blob_crc32c