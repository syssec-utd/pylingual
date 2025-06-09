import requests
import json
from netbluemind.python import serder
from netbluemind.python.client import BaseEndpoint
ICalendarView_VERSION = '4.1.64823'

class ICalendarView(BaseEndpoint):

    def __init__(self, apiKey, url, containerUid):
        self.url = url
        self.apiKey = apiKey
        self.base = url + '/calendars/view/{containerUid}'
        self.containerUid_ = containerUid
        self.base = self.base.replace('{containerUid}', containerUid)

    def multipleGet(self, uids):
        postUri = '/_mget'
        __data__ = None
        __encoded__ = None
        __data__ = serder.ListSerDer(serder.STRING).encode(uids)
        __encoded__ = json.dumps(__data__)
        queryParams = {}
        response = requests.post(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        from netbluemind.calendar.api.CalendarView import CalendarView
        from netbluemind.calendar.api.CalendarView import __CalendarViewSerDer__
        from netbluemind.core.container.model.ItemValue import ItemValue
        from netbluemind.core.container.model.ItemValue import __ItemValueSerDer__
        return self.handleResult__(serder.ListSerDer(__ItemValueSerDer__(__CalendarViewSerDer__())), response)

    def update(self, uid, view):
        postUri = '/{uid}'
        __data__ = None
        __encoded__ = None
        postUri = postUri.replace('{uid}', uid)
        from netbluemind.calendar.api.CalendarView import CalendarView
        from netbluemind.calendar.api.CalendarView import __CalendarViewSerDer__
        __data__ = __CalendarViewSerDer__().encode(view)
        __encoded__ = json.dumps(__data__)
        queryParams = {}
        response = requests.post(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)

    def list(self):
        postUri = '/_list'
        __data__ = None
        __encoded__ = None
        queryParams = {}
        response = requests.get(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        from netbluemind.calendar.api.CalendarView import CalendarView
        from netbluemind.calendar.api.CalendarView import __CalendarViewSerDer__
        from netbluemind.core.container.model.ItemValue import ItemValue
        from netbluemind.core.container.model.ItemValue import __ItemValueSerDer__
        from netbluemind.core.api.ListResult import ListResult
        from netbluemind.core.api.ListResult import __ListResultSerDer__
        return self.handleResult__(__ListResultSerDer__(__ItemValueSerDer__(__CalendarViewSerDer__())), response)

    def updates(self, changes):
        postUri = '/_mupdates'
        __data__ = None
        __encoded__ = None
        from netbluemind.calendar.api.CalendarViewChanges import CalendarViewChanges
        from netbluemind.calendar.api.CalendarViewChanges import __CalendarViewChangesSerDer__
        __data__ = __CalendarViewChangesSerDer__().encode(changes)
        __encoded__ = json.dumps(__data__)
        queryParams = {}
        response = requests.put(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)

    def delete(self, uid):
        postUri = '/{uid}'
        __data__ = None
        __encoded__ = None
        postUri = postUri.replace('{uid}', uid)
        queryParams = {}
        response = requests.delete(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)

    def setDefault(self, uid):
        postUri = '/{uid}/_asdefault'
        __data__ = None
        __encoded__ = None
        postUri = postUri.replace('{uid}', uid)
        queryParams = {}
        response = requests.post(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)

    def getComplete(self, uid):
        postUri = '/{uid}'
        __data__ = None
        __encoded__ = None
        postUri = postUri.replace('{uid}', uid)
        queryParams = {}
        response = requests.get(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        from netbluemind.calendar.api.CalendarView import CalendarView
        from netbluemind.calendar.api.CalendarView import __CalendarViewSerDer__
        from netbluemind.core.container.model.ItemValue import ItemValue
        from netbluemind.core.container.model.ItemValue import __ItemValueSerDer__
        return self.handleResult__(__ItemValueSerDer__(__CalendarViewSerDer__()), response)

    def create(self, uid, view):
        postUri = '/{uid}'
        __data__ = None
        __encoded__ = None
        postUri = postUri.replace('{uid}', uid)
        from netbluemind.calendar.api.CalendarView import CalendarView
        from netbluemind.calendar.api.CalendarView import __CalendarViewSerDer__
        __data__ = __CalendarViewSerDer__().encode(view)
        __encoded__ = json.dumps(__data__)
        queryParams = {}
        response = requests.put(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ICalendarView_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)