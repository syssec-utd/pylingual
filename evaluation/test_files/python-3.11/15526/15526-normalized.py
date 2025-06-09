def repositories(self):
    """
        Return a list of all repository objects in the repofiles in the repo folder specified
        :return:
        """
    for repo_path in self.path.glob('*.repo'):
        for id, repository in self._get_repo_file(repo_path).repositories:
            yield (id, repository)