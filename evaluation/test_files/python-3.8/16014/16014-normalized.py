def _prepare_file(self, finder, req_to_install):
    """Prepare a single requirements files.

        :return: A list of addition InstallRequirements to also install.
        """
    if req_to_install.editable:
        logger.info('Obtaining %s', req_to_install)
    else:
        assert req_to_install.satisfied_by is None
        if not self.ignore_installed:
            skip_reason = self._check_skip_installed(req_to_install, finder)
        if req_to_install.satisfied_by:
            assert skip_reason is not None, '_check_skip_installed returned None but req_to_install.satisfied_by is set to %r' % (req_to_install.satisfied_by,)
            logger.info('Requirement already %s: %s', skip_reason, req_to_install)
        elif req_to_install.link and req_to_install.link.scheme == 'file':
            path = url_to_path(req_to_install.link.url)
            logger.info('Processing %s', display_path(path))
        else:
            logger.info('Collecting %s', req_to_install)
    with indent_log():
        if req_to_install.editable:
            req_to_install.ensure_has_source_dir(self.src_dir)
            req_to_install.update_editable(not self.is_download)
            abstract_dist = make_abstract_dist(req_to_install)
            abstract_dist.prep_for_dist()
            if self.is_download:
                req_to_install.archive(self.download_dir)
        elif req_to_install.satisfied_by:
            abstract_dist = Installed(req_to_install)
        else:
            req_to_install.ensure_has_source_dir(self.build_dir)
            if os.path.exists(os.path.join(req_to_install.source_dir, 'setup.py')):
                raise PreviousBuildDirError("pip can't proceed with requirements '%s' due to a pre-existing build directory (%s). This is likely due to a previous installation that failed. pip is being responsible and not assuming it can delete this. Please delete it and try again." % (req_to_install, req_to_install.source_dir))
            req_to_install.populate_link(finder, self.upgrade)
            assert req_to_install.link
            try:
                download_dir = self.download_dir
                autodelete_unpacked = True
                if req_to_install.link.is_wheel and self.wheel_download_dir:
                    download_dir = self.wheel_download_dir
                if req_to_install.link.is_wheel:
                    if download_dir:
                        autodelete_unpacked = True
                    else:
                        autodelete_unpacked = False
                unpack_url(req_to_install.link, req_to_install.source_dir, download_dir, autodelete_unpacked, session=self.session)
            except requests.HTTPError as exc:
                logger.critical('Could not install requirement %s because of error %s', req_to_install, exc)
                raise InstallationError('Could not install requirement %s because of HTTP error %s for URL %s' % (req_to_install, exc, req_to_install.link))
            abstract_dist = make_abstract_dist(req_to_install)
            abstract_dist.prep_for_dist()
            if self.is_download:
                if req_to_install.link.scheme in vcs.all_schemes:
                    req_to_install.archive(self.download_dir)
            if not self.ignore_installed:
                req_to_install.check_if_exists()
            if req_to_install.satisfied_by:
                if self.upgrade or self.ignore_installed:
                    if not (self.use_user_site and (not dist_in_usersite(req_to_install.satisfied_by))):
                        req_to_install.conflicts_with = req_to_install.satisfied_by
                    req_to_install.satisfied_by = None
                else:
                    logger.info('Requirement already satisfied (use --upgrade to upgrade): %s', req_to_install)
        dist = abstract_dist.dist(finder)
        more_reqs = []

        def add_req(subreq):
            sub_install_req = InstallRequirement(str(subreq), req_to_install, isolated=self.isolated, wheel_cache=self._wheel_cache)
            more_reqs.extend(self.add_requirement(sub_install_req, req_to_install.name))
        if not self.has_requirement(req_to_install.name):
            self.add_requirement(req_to_install, None)
        if not self.ignore_dependencies:
            if req_to_install.extras:
                logger.debug('Installing extra requirements: %r', ','.join(req_to_install.extras))
            missing_requested = sorted(set(req_to_install.extras) - set(dist.extras))
            for missing in missing_requested:
                logger.warning("%s does not provide the extra '%s'", dist, missing)
            available_requested = sorted(set(dist.extras) & set(req_to_install.extras))
            for subreq in dist.requires(available_requested):
                add_req(subreq)
        self.reqs_to_cleanup.append(req_to_install)
        if not req_to_install.editable and (not req_to_install.satisfied_by):
            self.successfully_downloaded.append(req_to_install)
    return more_reqs