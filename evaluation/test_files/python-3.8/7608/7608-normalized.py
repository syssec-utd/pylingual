def get_jobs_url(self, job_id):
    """
        Returns the URL to check job status.

        :param job_id:
            The ID of the job to check.
        """
    return compat.urllib_parse.urlunsplit((self.uri.scheme, self.uri.netloc, self.uri.path.rstrip('/') + '/jobs/' + job_id, self.uri.query, self.uri.fragment))