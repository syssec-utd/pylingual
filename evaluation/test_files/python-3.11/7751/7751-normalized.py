def register_job(self, id, job):
    """ Registers a new job or updates an existing job

           https://www.nomadproject.io/docs/http/job.html

            arguments:
              - id
            returns: dict
            raises:
              - nomad.api.exceptions.BaseNomadException
              - nomad.api.exceptions.URLNotFoundNomadException
        """
    return self.request(id, json=job, method='post').json()