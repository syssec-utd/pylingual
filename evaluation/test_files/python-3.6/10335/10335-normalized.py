def get_git_repos(url, token, collection, project):
    """
    Returns a list of all git repos for the supplied project within the supplied collection
    """
    git_client = create_tfs_git_client('{url}/{collection_name}'.format(url=url, collection_name=collection.name), token)
    logger.debug('Retrieving Git Repos for Project: {project_name}'.format(project_name=project.name))
    return git_client.get_repositories(project.id)