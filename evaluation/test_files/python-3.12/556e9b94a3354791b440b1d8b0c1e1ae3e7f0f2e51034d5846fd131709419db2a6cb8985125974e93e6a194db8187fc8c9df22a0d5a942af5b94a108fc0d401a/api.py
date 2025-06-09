import requests
import os
import json
from hestia_earth.schema import SchemaType, NESTED_SEARCHABLE_KEYS
from .storage import _load_from_storage, _exists
from .request import request_url, api_url, api_access_token

def _match_key_value(key: str, value):
    first_key = key.split('.')[0]
    query = {'match': {key: value}}
    return {'nested': {'path': first_key, 'query': query}} if first_key in NESTED_SEARCHABLE_KEYS else query

def _retry_request_error(func, retry_max: int=5):
    err = None
    for _ in range(retry_max):
        try:
            return func()
        except json.decoder.JSONDecodeError as e:
            err = e
            continue
    raise err

def _safe_get_request(url: str, res_error=None):

    def exec():
        try:
            headers = {'Content-Type': 'application/json'}
            access_token = api_access_token()
            if access_token:
                headers['X-Access-Token'] = access_token
            return requests.get(url, headers=headers).json()
        except requests.exceptions.RequestException:
            return res_error
    return _retry_request_error(exec)

def _safe_post_request(url: str, body: dict, res_error={}):

    def exec():
        try:
            headers = {'Content-Type': 'application/json'}
            access_token = api_access_token()
            if access_token:
                headers['X-Access-Token'] = access_token
            return requests.post(url, json.dumps(body), headers=headers).json()
        except requests.exceptions.RequestException:
            return res_error
    return _retry_request_error(exec)

def node_type_to_url(node_type: SchemaType):
    return f'{(node_type if isinstance(node_type, str) else node_type.value)}s'.lower()

def node_to_path(node_type: SchemaType, node_id: str, data_state=None):
    jsonld_path = os.path.join(node_type if isinstance(node_type, str) else node_type.value, f'{node_id}.jsonld')
    return jsonld_path if data_state is None or data_state == 'original' or len(data_state) == 0 else os.path.join(data_state, jsonld_path)

def find_related(node_type: SchemaType, id: str, related_type: SchemaType, limit=100, offset=0, relationship=None):
    """
    Return the list of related Nodes by going through a "relationship".
    You can navigate the Hestia Graph Database using this method.

    Parameters
    ----------
    node_type
        The `@type` of the Node to start from. Example: use `SchemaType.Cycle` to find nodes related to a `Cycle`.
    id
        The `@id` of the Node to start from.
    related_type
        The other Node to which the relation should go to. Example: use `SchemaType.Source` to find `Source` related to
        `Cycle`.
    limit
        The limit of relationships to return. Asking for large number might result in timeouts.
    offset
        Use with limit to paginate through the results.
    relationship
        The relationship used to connect both Node. See the API for more information.
    """
    url = request_url(f'{api_url()}/{node_type_to_url(node_type)}/{id}/{node_type_to_url(related_type)}', limit=limit, offset=offset, relationship=relationship)
    response = _safe_get_request(url)
    return response.get('results', []) if type(response) == dict else response

def download_hestia(node_id: str, node_type=SchemaType.TERM, data_state='', mode='') -> dict:
    """
    Download a Node from the Hestia Database.

    Parameters
    ----------
    node_id
        The `@id` of the Node.
    node_type
        The `@type` of the Node.
    data_state
        Optional - the `dataState` of the Node.
        Possible values are: `recalculated` or `aggregated`.
        If not provided, defaults to the original version.
    mode
        Optional - use `csv` to download as a CSV file, `zip` to download as a ZIP file. Defaults to `JSON`.

    Returns
    -------
    JSON
        The `JSON` content of the Node.
    """

    def fallback():
        url = request_url(f'{api_url()}/{node_type_to_url(node_type)}/{node_id}', dataState=data_state, mode=mode)
        return _safe_get_request(url)
    try:
        jsonld_path = node_to_path(node_type, node_id, data_state)
        data = _load_from_storage(jsonld_path)
        return json.loads(data) if data else None
    except ImportError:
        return fallback()

def node_exists(node_id: str, node_type=SchemaType.TERM) -> bool:
    """
    Checks if a node exists on the Hestia Database.

    Parameters
    ----------
    node_id
        The `@id` of the Node.
    node_type
        The `@type` of the Node.

    Returns
    -------
    bool
        True if the node exists, False otherwise.
    """

    def fallback():
        url = request_url(f'{api_url()}/{node_type_to_url(node_type)}/{node_id}')
        result = _safe_get_request(url)
        return result is not None and '@id' in result
    try:
        return _exists(node_to_path(node_type, node_id))
    except ImportError:
        return fallback()

def search(query: dict, fields=['@type', '@id', 'name'], limit=10, offset=0, sort=None) -> list:
    """
    Executes a raw search on the Hestia Platform.

    Parameters
    ----------
    query
        The search engine is using ElasticSearch engine version 7:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html.
        All options can be used here.
    fields
        The list of fields to return. Example: ['@type', '@id']. Defaults to `['@type', '@id', 'name']`.
    limit
        Optional - limit the number of results to return. Defaults to `10`.
    offset
        Optional - use with limit to paginate the results. Defaults to `0`.
    sort : dict
        Sorting options. Please refer to the ElasticSearch version 7 documentation for use.

    Returns
    -------
    List[JSON]
        List of Nodes (as JSON) found.
    """
    return _safe_post_request(f'{api_url()}/search', {'query': query, 'limit': limit, 'offset': offset, 'fields': fields, **({'sort': sort} if sort is not None else {})}).get('results', [])

def find_node(node_type: SchemaType, args: dict, limit=10) -> list:
    """
    Finds nodes on the Hestia Platform.

    Parameters
    ----------
    node_type
        The `@type` of the Node.
    args
        Dictionary of key/value to exec search on. Example: use `{'bibliography.title': 'My biblio'}` on a
        `SchemaType.Source` to find all `Source`s having a `bibliography` with `title` == `My biblio`
    limit
        Optional - limit the number of results to return. Defaults to `10`.

    Returns
    -------
    List[JSON]
        List of Nodes (as JSON) found.
    """
    query_args = list(map(lambda key: _match_key_value(key, args.get(key)), args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    return search(query={'bool': {'must': must}}, limit=limit)

def find_node_exact(node_type: SchemaType, args: dict) -> dict:
    """
    Finds a single Node on the Hestia Platform.

    Parameters
    ----------
    node_type
        The `@type` of the Node.
    args
        Dictionary of key/value to exec search on. Example: use `{'bibliography.title': 'My biblio'}` on a
        `SchemaType.Source` to find all `Source`s having a `bibliography` with `title` == `My biblio`

    Returns
    -------
    JSON
        JSON of the node if found, else `None`.
    """
    query_args = list(map(lambda key: _match_key_value(f'{key}.keyword', args.get(key)), args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    results = search(query={'bool': {'must': must}}, limit=2)
    return results[0] if len(results) == 1 else None