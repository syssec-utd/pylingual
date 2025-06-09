def build_graph(self, project, site, subject, session, scan, size, email=None, invariants=Invariants.ALL, fiber_file=DEFAULT_FIBER_FILE, atlas_file=None, use_threads=False, callback=None):
    """
        Builds a graph using the graph-services endpoint.

        Arguments:
            project (str): The project to use
            site (str): The site in question
            subject (str): The subject's identifier
            session (str): The session (per subject)
            scan (str): The scan identifier
            size (str): Whether to return a big (grute.BIG) or small
                (grute.SMALL) graph. For a better explanation, see m2g.io.
            email (str : self.email)*: An email to notify
            invariants (str[]: Invariants.ALL)*: An array of invariants to
                compute. You can use the grute.Invariants class to construct a
                list, or simply pass grute.Invariants.ALL to compute them all.
            fiber_file (str: DEFAULT_FIBER_FILE)*: A local filename of an
                MRI Studio .dat file
            atlas_file (str: None)*: A local atlas file, in NIFTI .nii format.
                If none is specified, the Desikan atlas is used by default.
            use_threads (bool: False)*: Whether to run the download in a Python
                thread. If set to True, the call to `build_graph` will end
                quickly, and the `callback` will be called with the returned
                status-code of the restful call as its only argument.
            callback (function: None)*: The function to run upon completion of
                the call, if using threads. (Will not be called if use_threads
                is set to False.)

        Returns:
            HTTP Response if use_threads is False. Otherwise, None

        Raises:
            ValueError: When the supplied values are invalid (contain invalid
                characters, bad email address supplied, etc.)
            RemoteDataNotFoundError: When the data cannot be processed due to
                a server error.
        """
    if email is None:
        email = self.email
    if not set(invariants) <= set(Invariants.ALL):
        raise ValueError('Invariants must be a subset of Invariants.ALL.')
    if use_threads and callback is not None:
        if not hasattr(callback, '__call__'):
            raise ValueError('callback must be a function.')
        if len(inspect.getargspec(callback).args) != 1:
            raise ValueError('callback must take exactly 1 argument.')
    if size not in [self.BIG, self.SMALL]:
        raise ValueError('size must be either grute.BIG or grute.SMALL.')
    url = 'buildgraph/{}/{}/{}/{}/{}/{}/{}/{}/'.format(project, site, subject, session, scan, size, email, '/'.join(invariants))
    if ' ' in url:
        raise ValueError('Arguments must not contain spaces.')
    if use_threads:
        download_thread = threading.Thread(target=self._run_build_graph, args=[url, fiber_file, atlas_file, callback])
        download_thread.start()
    else:
        return self._run_build_graph(url, fiber_file, atlas_file)
    return