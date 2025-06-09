def build(self):
    """Build wheels."""
    self.requirement_set.prepare_files(self.finder)
    reqset = self.requirement_set.requirements.values()
    buildset = []
    for req in reqset:
        if req.is_wheel:
            logger.info('Skipping %s, due to already being wheel.', req.name)
        elif req.editable:
            logger.info('Skipping %s, due to being editable', req.name)
        else:
            buildset.append(req)
    if not buildset:
        return True
    logger.info('Building wheels for collected packages: %s', ', '.join([req.name for req in buildset]))
    with indent_log():
        (build_success, build_failure) = ([], [])
        for req in buildset:
            if self._build_one(req):
                build_success.append(req)
            else:
                build_failure.append(req)
    if build_success:
        logger.info('Successfully built %s', ' '.join([req.name for req in build_success]))
    if build_failure:
        logger.info('Failed to build %s', ' '.join([req.name for req in build_failure]))
    return len(build_failure) == 0