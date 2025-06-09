def _get_run_hash(self):
    """Gets the hash of the nextflow file"""
    pipeline_path = get_nextflow_filepath(self.log_file)
    pipeline_hash = hashlib.md5()
    with open(pipeline_path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(4096), b''):
            pipeline_hash.update(chunk)
    workdir = self.workdir.encode('utf8')
    hostname = socket.gethostname().encode('utf8')
    hardware_addr = str(uuid.getnode()).encode('utf8')
    dir_hash = hashlib.md5(workdir + hostname + hardware_addr)
    return pipeline_hash.hexdigest() + dir_hash.hexdigest()