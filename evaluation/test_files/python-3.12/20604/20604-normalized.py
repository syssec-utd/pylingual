def _build_package_finder(self, options, index_urls, session):
    """
        Create a package finder appropriate to this install command.
        This method is meant to be overridden by subclasses, not
        called directly.
        """
    return PackageFinder(find_links=options.find_links, index_urls=index_urls, use_wheel=options.use_wheel, allow_external=options.allow_external, allow_unverified=options.allow_unverified, allow_all_external=options.allow_all_external, trusted_hosts=options.trusted_hosts, allow_all_prereleases=options.pre, process_dependency_links=options.process_dependency_links, session=session)