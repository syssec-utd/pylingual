def get_bucket(self):
    """given a bucket name and a client that is initialized, get or
           create the bucket.
        """
    for attr in ['bucket_name', 's3']:
        if not hasattr(self, attr):
            bot.exit('client is missing attribute %s' % attr)
    self.bucket = None
    for bucket in self.s3.buckets.all():
        if bucket.name == self.bucket_name:
            self.bucket = bucket
    if self.bucket is None:
        self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)
        bot.info('Created bucket %s' % self.bucket.name)
    return self.bucket