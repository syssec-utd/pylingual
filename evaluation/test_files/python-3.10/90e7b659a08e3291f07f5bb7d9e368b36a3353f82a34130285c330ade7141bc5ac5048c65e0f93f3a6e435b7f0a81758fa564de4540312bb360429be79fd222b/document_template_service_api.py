from __future__ import absolute_import
import six
from whitelabelmachinename.api_client import ApiClient

class DocumentTemplateServiceApi:

    def __init__(self, configuration):
        self.api_client = ApiClient(configuration=configuration)

    def count(self, space_id, **kwargs):
        """Count

        Counts the number of items in the database as restricted by the given filter.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True.
        
        >>> thread = api.count(space_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param EntityQueryFilter filter: The filter which restricts the entities which are used to calculate the count.
        :return: int
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        kwargs['request_timeout'] = self.api_client.configuration.request_timeout
        if kwargs.get('async_req'):
            return self.count_with_http_info(space_id, **kwargs)
        else:
            data = self.count_with_http_info(space_id, **kwargs)
            return data

    def count_with_http_info(self, space_id, **kwargs):
        """Count

        Counts the number of items in the database as restricted by the given filter.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True.
        
        >>> thread = api.count_with_http_info(space_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param EntityQueryFilter filter: The filter which restricts the entities which are used to calculate the count.
        :return: int
                 If the method is called asynchronously,
                 returns the request thread.
        """
        all_params = ['space_id', 'filter']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('request_timeout')
        params = locals()
        for (key, val) in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method count" % key)
            params[key] = val
        del params['kwargs']
        if 'space_id' not in params or params['space_id'] is None:
            raise ValueError('Missing the required parameter `space_id` when calling `count`')
        collection_formats = {}
        path_params = {}
        query_params = []
        if 'space_id' in params:
            query_params.append(('spaceId', params['space_id']))
        header_params = {}
        form_params = []
        local_var_files = {}
        body_params = None
        if 'filter' in params:
            body_params = params['filter']
        header_params['Accept'] = self.api_client.select_header_accept(['application/json;charset=utf-8'])
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json;charset=utf-8'])
        auth_settings = []
        return self.api_client.call_api('/document-template/count', 'POST', path_params, query_params, header_params, body=body_params, post_params=form_params, files=local_var_files, response_type='int', auth_settings=auth_settings, async_req=params.get('async_req'), _return_http_data_only=params.get('_return_http_data_only'), _preload_content=params.get('_preload_content', True), _request_timeout=params.get('request_timeout'), collection_formats=collection_formats)

    def read(self, space_id, id, **kwargs):
        """Read

        Reads the entity with the given 'id' and returns it.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True.
        
        >>> thread = api.read(space_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param int id: The id of the document template which should be returned. (required)
        :return: DocumentTemplate
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        kwargs['request_timeout'] = self.api_client.configuration.request_timeout
        if kwargs.get('async_req'):
            return self.read_with_http_info(space_id, id, **kwargs)
        else:
            data = self.read_with_http_info(space_id, id, **kwargs)
            return data

    def read_with_http_info(self, space_id, id, **kwargs):
        """Read

        Reads the entity with the given 'id' and returns it.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True.
        
        >>> thread = api.read_with_http_info(space_id, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param int id: The id of the document template which should be returned. (required)
        :return: DocumentTemplate
                 If the method is called asynchronously,
                 returns the request thread.
        """
        all_params = ['space_id', 'id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('request_timeout')
        params = locals()
        for (key, val) in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method read" % key)
            params[key] = val
        del params['kwargs']
        if 'space_id' not in params or params['space_id'] is None:
            raise ValueError('Missing the required parameter `space_id` when calling `read`')
        if 'id' not in params or params['id'] is None:
            raise ValueError('Missing the required parameter `id` when calling `read`')
        collection_formats = {}
        path_params = {}
        query_params = []
        if 'space_id' in params:
            query_params.append(('spaceId', params['space_id']))
        if 'id' in params:
            query_params.append(('id', params['id']))
        header_params = {}
        form_params = []
        local_var_files = {}
        body_params = None
        header_params['Accept'] = self.api_client.select_header_accept(['application/json;charset=utf-8'])
        header_params['Content-Type'] = self.api_client.select_header_content_type(['*/*'])
        auth_settings = []
        return self.api_client.call_api('/document-template/read', 'GET', path_params, query_params, header_params, body=body_params, post_params=form_params, files=local_var_files, response_type='DocumentTemplate', auth_settings=auth_settings, async_req=params.get('async_req'), _return_http_data_only=params.get('_return_http_data_only'), _preload_content=params.get('_preload_content', True), _request_timeout=params.get('request_timeout'), collection_formats=collection_formats)

    def search(self, space_id, query, **kwargs):
        """Search

        Searches for the entities as specified by the given query.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True.
        
        >>> thread = api.search(space_id, query, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param EntityQuery query: The query restricts the document templates which are returned by the search. (required)
        :return: list[DocumentTemplate]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        kwargs['request_timeout'] = self.api_client.configuration.request_timeout
        if kwargs.get('async_req'):
            return self.search_with_http_info(space_id, query, **kwargs)
        else:
            data = self.search_with_http_info(space_id, query, **kwargs)
            return data

    def search_with_http_info(self, space_id, query, **kwargs):
        """Search

        Searches for the entities as specified by the given query.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True.
        
        >>> thread = api.search_with_http_info(space_id, query, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param EntityQuery query: The query restricts the document templates which are returned by the search. (required)
        :return: list[DocumentTemplate]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        all_params = ['space_id', 'query']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('request_timeout')
        params = locals()
        for (key, val) in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method search" % key)
            params[key] = val
        del params['kwargs']
        if 'space_id' not in params or params['space_id'] is None:
            raise ValueError('Missing the required parameter `space_id` when calling `search`')
        if 'query' not in params or params['query'] is None:
            raise ValueError('Missing the required parameter `query` when calling `search`')
        collection_formats = {}
        path_params = {}
        query_params = []
        if 'space_id' in params:
            query_params.append(('spaceId', params['space_id']))
        header_params = {}
        form_params = []
        local_var_files = {}
        body_params = None
        if 'query' in params:
            body_params = params['query']
        header_params['Accept'] = self.api_client.select_header_accept(['application/json;charset=utf-8'])
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json;charset=utf-8'])
        auth_settings = []
        return self.api_client.call_api('/document-template/search', 'POST', path_params, query_params, header_params, body=body_params, post_params=form_params, files=local_var_files, response_type='list[DocumentTemplate]', auth_settings=auth_settings, async_req=params.get('async_req'), _return_http_data_only=params.get('_return_http_data_only'), _preload_content=params.get('_preload_content', True), _request_timeout=params.get('request_timeout'), collection_formats=collection_formats)