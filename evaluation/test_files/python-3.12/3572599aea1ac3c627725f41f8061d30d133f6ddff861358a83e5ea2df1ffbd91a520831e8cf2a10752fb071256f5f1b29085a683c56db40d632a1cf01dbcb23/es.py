"""
####################################################
###########         dependency          ############
####################################################
pip install elasticsearch

####################################################
###########         config.yml          ############
####################################################
es:
  default:
    host: host-name
    port: 9200
    user: optional-username
    password: optional-password
    index: default-index
  some-other:
    host: hostname-b
    port: 59200
    index: default-index


####################################################
###########          usage              ############
####################################################
from hao.es import EsClient
es_client = EsClient()
es_client = EsClient('some-other')

es_client.delete_by_id(_id, index='optional-index')

es_client.save(_id, data, index='optional-index', silent=False)

es_client.update(_id, data, index='optional-index', silent=False)

es_client.is_exists(_id, index='optional-index')

es_client.get_by_id(_id, index='optional-index')

es_client.get_by_ids(id_list, index='optional-index')

count = es_client.count(query, index='optional-index')

# search once
items = es_client.search(query, index='optional-index', size=200)

# scrolls
items_generator = es_client.search(query, index='optional-index', size=200, scroll='10m')

es_client.delete_by_query(query, index='optional-index', timeout=600)

es_client.delete_by_id(id, index='optional-index')

es_client.bulk(actions)
"""
from elasticsearch import Elasticsearch, NotFoundError, helpers
from . import config, invoker, jsons, logs, slacks
LOGGER = logs.get_logger(__name__)

def connect(host, port, user=None, password=None, timeout=60) -> Elasticsearch:
    LOGGER.info(f'connecting to {host}:{port}')
    if user and password:
        return Elasticsearch(host, port=port, http_auth=(user, password), timeout=timeout)
    return Elasticsearch(host, port=port, timeout=timeout)

class EsClient(object):

    def __init__(self, profile='default'):
        self.profile = profile
        self.conf = config.get(f'es.{self.profile}')
        if self.conf is None:
            raise ValueError(f'profile not configured: {self.profile}')
        self.index = self.conf.get('index') or '_all'
        self.doc_type = self.conf.get('type') or '_doc'
        self.client: Elasticsearch = invoker.invoke(connect, **self.conf)

    def get_by_id(self, _id, index=None, **kwargs):
        try:
            index = index or self.index
            return self.client.get(index=index, doc_type='_all', id=_id, **kwargs)
        except NotFoundError:
            return None

    def get_by_ids(self, _ids, index=None, **kwargs):
        try:
            index = index or self.index
            result = self.client.mget(index=index, doc_type='_all', body={'ids': _ids}, **kwargs)
            return result.get('docs') if result else None
        except NotFoundError:
            return None

    def count(self, query: dict, index=None, **params):
        if query is None or len(query) == 0:
            LOGGER.warning('empty query')
            return 0
        index = index or self.index
        body = query.copy()
        for field in ['track_total_hits', 'from', 'size', '_source', 'sort', 'highlight']:
            body.pop(field, None)
        data = self.client.count(index=index, body=body, params=params)
        return data['count']

    def search(self, query: dict, index=None, size=500, scroll=None, timeout=60):
        if query is None or len(query) == 0:
            LOGGER.warning('empty query')
            return None
        index = index or self.index
        if scroll is None or len(scroll) == 0:
            data = self.client.search(index=index, size=size, body=query, request_timeout=timeout)
            hits = data['hits']['hits']
            for hit in hits:
                yield hit
        else:
            data = self.client.search(index=index, scroll=scroll, size=size, body=query, request_timeout=timeout)
            sid = data['_scroll_id']
            hits = data['hits']['hits']
            try:
                while sid and hits:
                    for hit in hits:
                        yield hit
                    data = self.client.scroll(scroll_id=sid, scroll=scroll)
                    sid = data['_scroll_id']
                    hits = data['hits']['hits']
            finally:
                try:
                    self.client.clear_scroll(scroll_id=sid, ignore=(404,))
                except Exception as ignored:
                    pass

    def aggs(self, query: dict, index=None, timeout=15):
        if query is None or len(query) == 0:
            LOGGER.warning('empty query')
            return None
        index = index or self.index
        data = self.client.search(index=index, size=0, body=query, request_timeout=timeout)
        buckets = {k: v.get('buckets') for k, v in data.get('aggregations').items()}
        total = data['hits']['total']
        return (buckets, total)

    def delete_by_id(self, _id, index=None, doc_type=None, silent=True, timeout=30) -> bool:
        try:
            index = index or self.index
            doc_type = doc_type or self.doc_type
            self.client.delete(index=index, doc_type=doc_type, id=_id, request_timeout=timeout)
            return True
        except NotFoundError as e:
            if silent:
                return False
            else:
                raise e

    def delete_by_query(self, query, index=None, doc_type=None, silent=True, timeout=30):
        try:
            index = index or self.index
            doc_type = doc_type or self.doc_type
            return self.client.delete_by_query(index=index, body=query, doc_type=doc_type, request_timeout=timeout)
        except NotFoundError as e:
            if silent:
                LOGGER.error(f'Failed to delete_by_query: {query}, index: {index}')
                LOGGER.exception(e)
                slacks.notify_exception(e, f'{jsons.dumps(query)}, index: {index}')
            else:
                raise e

    def save(self, _id, doc, index=None, doc_type=None, overwrite=True, silent: bool=True):
        if doc is None:
            return
        try:
            index = index or self.index
            doc_type = doc_type or self.doc_type
            if not overwrite and self.is_exists(_id, index=index, doc_type=doc_type):
                return
            self.client.index(index, doc, doc_type=doc_type, id=_id)
            return _id
        except Exception as e:
            if silent:
                LOGGER.error(f'Failed to process: {doc}')
                LOGGER.exception(e)
                slacks.notify_exception(e, f'{_id}\n{jsons.dumps(doc)}')
            else:
                raise e

    def update(self, _id, doc, index=None, doc_type=None):
        index = index or self.index
        doc_type = doc_type or self.doc_type
        self.client.update(index, doc_type=doc_type, id=_id, body={'doc': doc})

    def is_exists(self, _id, index=None, doc_type=None, source=False):
        index = index or self.index
        doc_type = doc_type or self.doc_type
        return self.client.exists(index=index, doc_type=doc_type, id=_id, _source=source)

    def bulk(self, actions, stats_only=False, *args, **kwargs):
        helpers.bulk(self.client, actions, *args, stats_only=stats_only, **kwargs)