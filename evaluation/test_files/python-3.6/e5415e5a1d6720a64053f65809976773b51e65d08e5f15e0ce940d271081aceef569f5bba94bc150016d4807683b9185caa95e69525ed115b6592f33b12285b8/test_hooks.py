from plone.caching.hooks import intercept
from plone.caching.hooks import Intercepted
from plone.caching.hooks import InterceptorResponse
from plone.caching.hooks import modifyStreamingResponse
from plone.caching.hooks import MutatorTransform
from plone.caching.interfaces import ICacheSettings
from plone.caching.interfaces import ICachingOperation
from plone.caching.interfaces import IRulesetLookup
from plone.caching.lookup import DefaultRulesetLookup
from plone.caching.testing import IMPLICIT_RULESET_REGISTRY_UNIT_TESTING
from plone.registry import Registry
from plone.registry.fieldfactory import persistentFieldAdapter
from plone.registry.interfaces import IRegistry
from ZODB.POSException import ConflictError
from zope.component import adapter
from zope.component import getUtility
from zope.component import provideAdapter
from zope.component import provideUtility
from zope.globalrequest import clearRequest
from zope.globalrequest import setRequest
from zope.interface import implementer
from zope.interface import Interface
import unittest
import z3c.caching.registry

class DummyView:
    pass

class DummyResource:

    def index_html(self):
        return b'binary data'

class DummyResponse(dict):
    locked = None

    def addHeader(self, name, value):
        self.setdefault(name, []).append(value)

    def setHeader(self, name, value):
        self[name] = [value]

    def setStatus(self, value, lock=None):
        self.status = value
        if lock is not None:
            self.locked = lock

    def getStatus(self):
        return self.status

class DummyRequest(dict):

    def __init__(self, published, response):
        self['PUBLISHED'] = published
        self.response = response
        self.environ = {}

class DummyEvent:

    def __init__(self, request):
        self.request = request

class DummyStreamingEvent:

    def __init__(self, response):
        self.response = response

class TestMutateResponse(unittest.TestCase):
    layer = IMPLICIT_RULESET_REGISTRY_UNIT_TESTING

    def setUp(self):
        provideAdapter(persistentFieldAdapter)

    def test_no_published_object(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        request = DummyRequest(None, DummyResponse())
        MutatorTransform(None, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': None}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_registry(self):
        provideAdapter(DefaultRulesetLookup)
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_records(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_mapping(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_cache_rule(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        settings.operationMapping = {'testrule': 'dummy'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_lookup_adapter(self):
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'dummy'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_operation_name_not_found(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'foo': 'bar'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule']}, dict(request.response))

    def test_operation_not_found(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'notfound'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule']}, dict(request.response))

    def test_match_unicode(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_bytes(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformBytes('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_iterable(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformIterable([''], 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_method(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyResource, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        resource = DummyResource()
        request = DummyRequest(resource.index_html, DummyResponse())
        MutatorTransform(resource, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': resource.index_html}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_off_switch(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = False
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response['X-Mutated'] = rulename
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        MutatorTransform(view, request).transformUnicode('', 'utf-8')
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

class TestMutateResponseStreaming(unittest.TestCase):
    layer = IMPLICIT_RULESET_REGISTRY_UNIT_TESTING

    def setUp(self):
        provideAdapter(persistentFieldAdapter)

    def tearDown(self):
        clearRequest()

    def test_no_published_object(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        response = DummyResponse()
        request = DummyRequest(None, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': None}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_registry(self):
        provideAdapter(DefaultRulesetLookup)
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_records(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_mapping(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_cache_rule(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        settings.operationMapping = {'testrule': 'dummy'}
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_lookup_adapter(self):
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'dummy'}
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_operation_name_not_found(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'foo': 'bar'}
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule']}, dict(request.response))

    def test_operation_not_found(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'notfound'}
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule']}, dict(request.response))

    def test_match_unicode(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_bytes(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_iterable(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_method(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyResource, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
        provideAdapter(DummyOperation, name='op1')
        resource = DummyResource()
        response = DummyResponse()
        request = DummyRequest(resource.index_html, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': resource.index_html}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_off_switch(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = False
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def interceptResponse(self, rulename, response):
                return None

            def modifyResponse(self, rulename, response):
                response['X-Mutated'] = rulename
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        response = DummyResponse()
        request = DummyRequest(view, response)
        setRequest(request)
        modifyStreamingResponse(DummyStreamingEvent(response))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

class TestIntercept(unittest.TestCase):
    layer = IMPLICIT_RULESET_REGISTRY_UNIT_TESTING

    def setUp(self):
        provideAdapter(persistentFieldAdapter)

    def test_no_published_object(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        request = DummyRequest(None, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': None}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_registry(self):
        provideAdapter(DefaultRulesetLookup)
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_records(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_cache_rule(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        settings.operationMapping = {'testrule': 'dummy'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_no_mapping(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        settings.operationMapping = None
        z3c.caching.registry.register(DummyView, 'testrule')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_operation_not_found(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'notfound'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule']}, dict(request.response))

    def test_match_abort(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def modifyResponse(self, rulename, response):
                pass

            def interceptResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
                return None
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_body(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def modifyResponse(self, rulename, response):
                pass

            def interceptResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
                response.setStatus(304)
                return 'dummy'
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        try:
            intercept(DummyEvent(request))
            self.fail()
        except Intercepted as e:
            self.assertEqual('dummy', e.responseBody)
            self.assertEqual(304, e.status)
            self.assertEqual(304, request.response.status)
            self.assertEqual(True, request.response.locked)
        except Exception as e:
            self.fail(str(e))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'plone.transformchain.disable': True}, request.environ)
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_body_explicitly_enable_transform_chain(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def modifyResponse(self, rulename, response):
                pass

            def interceptResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
                response.setStatus(304)
                self.request.environ['plone.transformchain.disable'] = False
                return 'dummy'
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        try:
            intercept(DummyEvent(request))
            self.fail()
        except Intercepted as e:
            self.assertEqual('dummy', e.responseBody)
            self.assertEqual(304, e.status)
            self.assertEqual(304, request.response.status)
            self.assertEqual(True, request.response.locked)
        except Exception as e:
            self.fail(str(e))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({'plone.transformchain.disable': False}, request.environ)
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_match_body_method(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        z3c.caching.registry.register(DummyResource, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def modifyResponse(self, rulename, response):
                pass

            def interceptResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
                response.setStatus(200)
                return 'dummy'
        provideAdapter(DummyOperation, name='op1')
        resource = DummyResource()
        request = DummyRequest(resource.index_html, DummyResponse())
        try:
            intercept(DummyEvent(request))
            self.fail()
        except Intercepted as e:
            self.assertEqual('dummy', e.responseBody)
            self.assertEqual(200, e.status)
            self.assertEqual(200, request.response.status)
            self.assertEqual(True, request.response.locked)
        except Exception as e:
            self.fail(str(e))
        self.assertEqual({'PUBLISHED': resource.index_html}, dict(request))
        self.assertEqual({'plone.transformchain.disable': True}, request.environ)
        self.assertEqual({'X-Cache-Rule': ['testrule'], 'X-Cache-Operation': ['op1'], 'X-Cache-Foo': ['test']}, dict(request.response))

    def test_off_switch(self):
        provideAdapter(DefaultRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = False
        z3c.caching.registry.register(DummyView, 'testrule')
        settings.operationMapping = {'testrule': 'op1'}

        @implementer(ICachingOperation)
        @adapter(Interface, Interface)
        class DummyOperation:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def modifyResponse(self, rulename, response):
                pass

            def interceptResponse(self, rulename, response):
                response.addHeader('X-Cache-Foo', 'test')
                return 'dummy'
        provideAdapter(DummyOperation, name='op1')
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        intercept(DummyEvent(request))
        self.assertEqual({'PUBLISHED': view}, dict(request))
        self.assertEqual({}, dict(request.response))

    def test_dont_swallow_conflict_error(self):

        @implementer(IRulesetLookup)
        @adapter(Interface, Interface)
        class DummyRulesetLookup:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def __call__(self):
                raise ConflictError()
        provideAdapter(DummyRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        settings.operationMapping = {'foo': 'bar'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        self.assertRaises(ConflictError, intercept, DummyEvent(request))

    def test_swallow_other_error(self):

        @implementer(IRulesetLookup)
        @adapter(Interface, Interface)
        class DummyRulesetLookup:

            def __init__(self, published, request):
                self.published = published
                self.request = request

            def __call__(self):
                raise AttributeError('Should be swallowed and logged')
        provideAdapter(DummyRulesetLookup)
        provideUtility(Registry(), IRegistry)
        registry = getUtility(IRegistry)
        registry.registerInterface(ICacheSettings)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        settings.operationMapping = {'foo': 'bar'}
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        try:
            intercept(DummyEvent(request))
        except Exception:
            self.fail('Intercept should not raise')

    def test_exception_view(self):
        view = DummyView()
        request = DummyRequest(view, DummyResponse())
        exc = Intercepted(status=200, responseBody='Test')
        excView = InterceptorResponse(exc, request)
        self.assertEqual('Test', excView())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)