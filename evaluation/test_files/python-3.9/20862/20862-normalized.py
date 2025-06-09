def start(self, n):
    """Start n copies of the process using the Win HPC job scheduler."""
    self.write_job_file(n)
    args = ['submit', '/jobfile:%s' % self.job_file, '/scheduler:%s' % self.scheduler]
    self.log.debug('Starting Win HPC Job: %s' % (self.job_cmd + ' ' + ' '.join(args),))
    output = check_output([self.job_cmd] + args, env=os.environ, cwd=self.work_dir, stderr=STDOUT)
    job_id = self.parse_job_id(output)
    self.notify_start(job_id)
    return job_id