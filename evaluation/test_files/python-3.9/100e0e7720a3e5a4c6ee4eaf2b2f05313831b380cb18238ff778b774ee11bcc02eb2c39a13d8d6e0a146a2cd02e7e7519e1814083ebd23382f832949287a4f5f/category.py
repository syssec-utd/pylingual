"""
WPTools Category module
~~~~~~~~~~~~~~~~~~~~~~~

Support for getting Mediawiki category info.
"""
from . import core

class WPToolsCategory(core.WPTools):
    """
    WPToolsCategory class
    """

    def __init__(self, *args, **kwargs):
        """
        Returns a WPToolsCategory object

        Gets a random category without arguments

        Optional positional {params}:
        - [title]: <str> category title

        Optional keyword {params}:
        - [endpoint]: <str> alternative API endpoint (default=/w/api.php)
        - [lang]: <str> Mediawiki language code (default=en)
        - [namespace]: <int> filter members (0=article, 14=category)
        - [pageid]: <int> category pageid
        - [variant]: <str> Mediawiki language variant
        - [wiki]: <str> alternative wiki site (default=wikipedia.org)

        Optional keyword {flags}:
        - [silent]: <bool> do not echo page data if True
        - [skip]: <list> skip actions in this list
        - [verbose]: <bool> verbose output to stderr if True

        See also:
        https://www.mediawiki.org/wiki/Manual:Namespace
        """
        super(WPToolsCategory, self).__init__(**kwargs)
        endpoint = kwargs.get('endpoint')
        pageid = kwargs.get('pageid')
        namespace = kwargs.get('namespace')
        title = None
        if len(args) > 0:
            title = args[0]
            self.params.update({'title': title})
        if endpoint:
            self.params.update({'endpoint': endpoint})
        if pageid:
            try:
                self.params.update({'pageid': int(pageid)})
            except ValueError:
                raise ValueError('invalid pageid')
            if title:
                raise ValueError('cannot use both title AND pageid')
        if namespace or namespace == 0:
            try:
                self.params.update({'namespace': int(namespace)})
            except ValueError:
                raise ValueError('invalid namespace')
        if not pageid and (not title):
            self.get_random()

    def _add_members(self, catmembers):
        """
        Adds category members and subcategories to data
        """
        members = [x for x in catmembers if x['ns'] == 0]
        subcats = [x for x in catmembers if x['ns'] == 14]
        if 'members' in self.data:
            self.data['members'].extend(members)
        else:
            self.data.update({'members': members})
        if subcats:
            if 'subcategories' in self.data:
                self.data['subcategories'].extend(subcats)
            else:
                self.data.update({'subcategories': subcats})

    def _query(self, action, qobj):
        """
        Form query to enumerate category
        """
        title = self.params.get('title')
        pageid = self.params.get('pageid')
        if action == 'random':
            return qobj.random(namespace=14)
        elif action == 'category':
            return qobj.category(title, pageid, self._continue_params())

    def _set_data(self, action):
        """
        Set category member data from API response
        """
        data = self._load_response(action)
        self._handle_continuations(data, 'category')
        if action == 'category':
            members = data.get('query').get('categorymembers')
            if members:
                self._add_members(members)
        if action == 'random':
            rand = data['query']['random'][0]
            data = {'pageid': rand.get('id'), 'title': rand.get('title')}
            self.data.update(data)
            self.params.update(data)

    def get_members(self, show=True, proxy=None, timeout=0):
        """
        GET Mediawiki:API (action=query) category members
        https://www.mediawiki.org/wiki/API:Categorymembers

        Required {params}: title OR pageid
        - title: <str> article title
        - pageid: <int> Wikipedia database ID

        Optional arguments:
        - [show]: <bool> echo page data if true
        - [proxy]: <str> use this HTTP proxy
        - [timeout]: <int> timeout in seconds (0=wait forever)

        Data captured:
        - members: <list> category members [{ns, pageid, title}]
        """
        title = self.params.get('title')
        pageid = self.params.get('pageid')
        if not title and (not pageid):
            raise LookupError('needs category title or pageid')
        self._get('category', show, proxy, timeout)
        while self.data.get('continue'):
            self._get('category', show, proxy, timeout)
        return self

    def get_random(self, show=True, proxy=None, timeout=0):
        """
        GET MediaWiki:API (action=query) for random category
        https://www.mediawiki.org/wiki/API:Random

        Required {params}: None

        Optional arguments:
        - [show]: <bool> echo page data if true
        - [proxy]: <str> use this HTTP proxy
        - [timeout]: <int> timeout in seconds (0=wait forever)

        Data captured:
        - pageid: <int> Wikipedia database ID
        - title: <str> article title
        """
        self._get('random', show, proxy, timeout)
        del self.cache['random']
        return self