def _init_client(self):
    """init client will check if the user has defined a bucket that
           differs from the default, use the application credentials to 
           get the bucket, and then instantiate the client.
        """
    self._get_services()
    env = 'SREGISTRY_GOOGLE_STORAGE_BUCKET'
    self._bucket_name = self._get_and_update_setting(env)
    if self._bucket_name is None:
        self._bucket_name = 'sregistry-%s' % os.environ['USER']
    self._get_bucket()