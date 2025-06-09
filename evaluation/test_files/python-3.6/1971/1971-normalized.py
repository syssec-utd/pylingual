def join(self):
    """Wait until job's completion."""
    self._future = False
    self._job.poll()
    model_key = self._job.dest_key
    self._job = None
    model_json = h2o.api('GET /%d/Models/%s' % (self._rest_version, model_key))['models'][0]
    self._resolve_model(model_key, model_json)