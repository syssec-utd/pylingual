def get_pull_request(app, repo_config, pull_request):
    """Data for a given pull request.

    :param app: Flask app
    :param repo_config: dict with ``github_repo`` key
    :param pull_request: the pull request number
    """
    response = get_api_response(app, repo_config, '/repos/{{repo_name}}/pulls/{0}'.format(pull_request))
    if not response.ok:
        raise Exception('Unable to get pull request: status code {}'.format(response.status_code))
    return response.json