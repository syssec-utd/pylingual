def _submitQuery(self, gitquery, gitvars={}, verbose=False, rest=False):
    """Send a curl request to GitHub.

        Args:
            gitquery (str): The query or endpoint itself.
                Examples:
                       query: 'query { viewer { login } }'
                    endpoint: '/user'
            gitvars (Optional[Dict]): All query variables.
                Defaults to empty.
            verbose (Optional[bool]): If False, stderr prints will be
                suppressed. Defaults to False.
            rest (Optional[bool]): If True, uses the REST API instead
                of GraphQL. Defaults to False.

        Returns:
            {
                'statusNum' (int): The HTTP status code.
                'headDict' (Dict[str]): The response headers.
                'linkDict' (Dict[int]): Link based pagination data.
                'result' (str): The body of the response.
            }

        """
    errOut = DEVNULL if not verbose else None
    authhead = 'Authorization: bearer ' + self.__githubApiToken
    bashcurl = 'curl -iH TMPauthhead -X POST -d TMPgitquery https://api.github.com/graphql' if not rest else 'curl -iH TMPauthhead https://api.github.com' + gitquery
    bashcurl_list = bashcurl.split()
    bashcurl_list[2] = authhead
    if not rest:
        gitqueryJSON = json.dumps({'query': gitquery, 'variables': json.dumps(gitvars)})
        bashcurl_list[6] = gitqueryJSON
    fullResponse = check_output(bashcurl_list, stderr=errOut).decode()
    _vPrint(verbose, '\n' + fullResponse)
    fullResponse = fullResponse.split('\r\n\r\n')
    heads = fullResponse[0].split('\r\n')
    if len(fullResponse) > 1:
        result = fullResponse[1]
    else:
        result = ''
    http = heads[0].split()
    statusNum = int(http[1])
    headDict = {}
    headDict['http'] = heads[0]
    for header in heads[1:]:
        h = header.split(': ')
        headDict[h[0]] = h[1]
    linkDict = None
    if 'Link' in headDict:
        linkProperties = headDict['Link'].split(', ')
        propDict = {}
        for item in linkProperties:
            divided = re.split('<https://api.github.com|>; rel="|"', item)
            propDict[divided[2]] = divided[1]
        linkDict = propDict
    return {'statusNum': statusNum, 'headDict': headDict, 'linkDict': linkDict, 'result': result}