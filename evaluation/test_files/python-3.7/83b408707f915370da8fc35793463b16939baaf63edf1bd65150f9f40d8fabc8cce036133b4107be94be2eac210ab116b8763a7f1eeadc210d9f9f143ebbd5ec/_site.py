from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from netlink.logging import logger

class Site:
    _url = ''
    _id = ''
    _secret = ''

    def __init__(self, url=None, client_id=None, client_secret=None):
        self._context = ClientContext(url or self._url).with_credentials(ClientCredential(client_id=client_id or self._id, client_secret=client_secret or self._secret))
        self._users = None
        self._lists = {}

    def get_list(self, name):
        if name not in self._lists:
            self._lists[name] = self._context.web.lists.get_by_title(name)
        return self._lists[name]

    @property
    def url(self):
        return self._context.base_url

    def get_lists(self, hidden=False):
        if hidden:
            selector = lambda x: True
        else:
            selector = lambda x: x.properties['BaseTemplate'] == 100 and x.title not in ('TaxonomyHiddenList',)
        return [i for i in self._context.lists.get().execute_query() if selector(i)]

    def get_list_items(self, name):
        return self.get_list(name).items.get().execute_query()

    def commit(self):
        self._context.execute_batch()

    def get_list_columns(self, name, hidden=False):
        if not isinstance(name, str):
            name = name.title
        if hidden:
            selector = lambda x: True
        else:
            selector = lambda x: not x.hidden and x.group not in ('_Hidden',) and (not x.internal_name.startswith('_')) and (x.internal_name not in ('Edit', 'LinkTitleNoMenu', 'LinkTitle', 'DocIcon', 'ItemChildCount', 'FolderChildCount', 'AppAuthor', 'AppEditor', 'ComplianceAssetId', 'Modified', 'Created', 'Author', 'Editor', 'Attachments'))
        return [i for i in self.get_list(name).fields.get().execute_query() if selector(i)]