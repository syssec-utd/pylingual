def stop_cluster(self, profile):
    """Stop a cluster for a given profile."""
    self.check_profile(profile)
    data = self.profiles[profile]
    if data['status'] == 'stopped':
        raise web.HTTPError(409, u'cluster not running')
    data = self.profiles[profile]
    cl = data['controller_launcher']
    esl = data['engine_set_launcher']
    if cl.running:
        cl.stop()
    if esl.running:
        esl.stop()
    result = {'profile': data['profile'], 'profile_dir': data['profile_dir'], 'status': 'stopped'}
    return result