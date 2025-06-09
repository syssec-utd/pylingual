def get_conversation_paged_members(self, conversation_id, page_size=None, continuation_token=None, custom_headers=None, raw=False, **operation_config):
    """GetConversationPagedMembers.

        Enumerate the members of a conversation one page at a time.
        This REST API takes a ConversationId. Optionally a pageSize and/or
        continuationToken can be provided. It returns a PagedMembersResult,
        which contains an array
        of ChannelAccounts representing the members of the conversation and a
        continuation token that can be used to get more values.
        One page of ChannelAccounts records are returned with each call. The
        number of records in a page may vary between channels and calls. The
        pageSize parameter can be used as
        a suggestion. If there are no additional results the response will not
        contain a continuation token. If there are no members in the
        conversation the Members will be empty or not present in the response.
        A response to a request that has a continuation token from a prior
        request may rarely return members from a previous request.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param page_size: Suggested page size
        :type page_size: int
        :param continuation_token: Continuation Token
        :type continuation_token: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PagedMembersResult or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.PagedMembersResult or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
    url = self.get_conversation_paged_members.metadata['url']
    path_format_arguments = {'conversationId': self._serialize.url('conversation_id', conversation_id, 'str')}
    url = self._client.format_url(url, **path_format_arguments)
    query_parameters = {}
    if page_size is not None:
        query_parameters['pageSize'] = self._serialize.query('page_size', page_size, 'int')
    if continuation_token is not None:
        query_parameters['continuationToken'] = self._serialize.query('continuation_token', continuation_token, 'str')
    header_parameters = {}
    header_parameters['Accept'] = 'application/json'
    if custom_headers:
        header_parameters.update(custom_headers)
    request = self._client.get(url, query_parameters, header_parameters)
    response = self._client.send(request, stream=False, **operation_config)
    if response.status_code not in [200]:
        raise HttpOperationError(self._deserialize, response)
    deserialized = None
    if response.status_code == 200:
        deserialized = self._deserialize('PagedMembersResult', response)
    if raw:
        client_raw_response = ClientRawResponse(deserialized, response)
        return client_raw_response
    return deserialized