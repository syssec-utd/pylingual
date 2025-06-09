def del_files(self, source):
    """Delete files on S3"""
    src_files = []
    for obj in self.s3walk(source):
        if not obj['is_dir']:
            src_files.append(obj['name'])
    pool = ThreadPool(ThreadUtil, self.opt)
    pool.batch_delete(src_files)
    pool.join()