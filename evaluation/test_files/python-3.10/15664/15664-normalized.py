def s3am_upload_job(job, file_id, file_name, s3_dir, s3_key_path=None):
    """Job version of s3am_upload"""
    work_dir = job.fileStore.getLocalTempDir()
    fpath = job.fileStore.readGlobalFile(file_id, os.path.join(work_dir, file_name))
    s3am_upload(job=job, fpath=fpath, s3_dir=s3_dir, num_cores=job.cores, s3_key_path=s3_key_path)