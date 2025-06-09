def get_size(self, bucket_name, object_name):
    """
        Gets the size of a file in Google Cloud Storage.

        :param bucket_name: The Google cloud storage bucket where the blob_name is.
        :type bucket_name: str
        :param object_name: The name of the object to check in the Google
            cloud storage bucket_name.
        :type object_name: str

        """
    self.log.info('Checking the file size of object: %s in bucket_name: %s', object_name, bucket_name)
    client = self.get_conn()
    bucket = client.get_bucket(bucket_name=bucket_name)
    blob = bucket.get_blob(blob_name=object_name)
    blob.reload()
    blob_size = blob.size
    self.log.info('The file size of %s is %s bytes.', object_name, blob_size)
    return blob_size