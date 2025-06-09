def sync(self, folders):
    """Syncs a list of folders to their assicated buckets.
        
        folders: A list of 2-tuples in the form (folder, bucket)
        """
    if not folders:
        raise ValueError('No folders to sync given')
    for folder in folders:
        self.sync_folder(*folder)