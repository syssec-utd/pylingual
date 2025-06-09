import unittest
from BTrees.IIBTree import difference
from OFS.SimpleItem import SimpleItem
from Testing.makerequest import makerequest
from Products.ZCatalog.query import IndexQuery

class TestUnIndex(unittest.TestCase):

    def _getTargetClass(self):
        from Products.PluginIndexes.unindex import UnIndex
        return UnIndex

    def _makeOne(self, *args, **kw):
        index = self._getTargetClass()(*args, **kw)

        class DummyZCatalog(SimpleItem):
            id = 'DummyZCatalog'
        catalog = makerequest(DummyZCatalog())
        indexes = SimpleItem()
        indexes = indexes.__of__(catalog)
        index = index.__of__(indexes)
        return index

    def _makeConflicted(self):
        from ZODB.POSException import ConflictError

        class Conflicted:

            def __str__(self):
                return 'Conflicted'
            __repr__ = __str__

            def __getattr__(self, id, default=object()):
                raise ConflictError('testing')
        return Conflicted()

    def test_empty(self):
        unindex = self._makeOne(id='empty')
        self.assertEqual(unindex.indexed_attrs, ['empty'])

    def test_removeForwardIndexEntry_with_ConflictError(self):
        from ZODB.POSException import ConflictError
        unindex = self._makeOne(id='conflicted')
        unindex._index['conflicts'] = self._makeConflicted()
        self.assertRaises(ConflictError, unindex.removeForwardIndexEntry, 'conflicts', 42)

    def test_get_object_datum(self):
        from Products.PluginIndexes.unindex import _marker
        idx = self._makeOne('interesting')
        dummy = object()
        self.assertEqual(idx._get_object_datum(dummy, 'interesting'), _marker)

        class DummyContent2:
            interesting = 'GOT IT'
        dummy = DummyContent2()
        self.assertEqual(idx._get_object_datum(dummy, 'interesting'), 'GOT IT')

        class DummyContent3:
            exc = None

            def interesting(self):
                if self.exc:
                    raise self.exc
                return 'GOT IT'
        dummy = DummyContent3()
        self.assertEqual(idx._get_object_datum(dummy, 'interesting'), 'GOT IT')
        dummy.exc = AttributeError
        self.assertEqual(idx._get_object_datum(dummy, 'interesting'), _marker)
        dummy.exc = TypeError
        self.assertEqual(idx._get_object_datum(dummy, 'interesting'), _marker)

    def test_cache(self):
        idx = self._makeOne(id='foo')
        idx.query_options = ('query', 'range', 'not', 'operator')

        def testQuery(record, expect=1):
            cache = idx.getRequestCache()
            cache.clear()
            res1 = idx._apply_index(record)
            self.assertEqual(cache._sets, expect)
            self.assertEqual(cache._misses, expect)
            res2 = idx._apply_index(record)
            self.assertEqual(cache._hits, expect)
            result = difference(res1[0], res2[0])
            self.assertEqual(len(result), 0)
        record = {'foo': {'query': ['e', 'f'], 'operator': 'or'}}
        testQuery(record)
        record = {'foo': {'query': ['e', 'f'], 'operator': 'and'}}
        testQuery(record)
        record = {'foo': {'query': ('abc', 'abcd'), 'range': 'min:max'}}
        testQuery(record)
        record = {'foo': {'query': ['a', 'ab'], 'not': 'a'}}
        testQuery(record)

    def test_getCounter(self):
        index = self._makeOne('counter')
        self.assertEqual(index.getCounter(), 0)

        class Dummy:
            id = 1
            counter = 'counter'
        obj = Dummy()
        index.index_object(obj.id, obj)
        self.assertEqual(index.getCounter(), 1)
        index.unindex_object(obj.id)
        self.assertEqual(index.getCounter(), 2)
        index.unindex_object(1234)
        self.assertEqual(index.getCounter(), 2)
        index.clear()
        self.assertEqual(index.getCounter(), 3)

    def test_no_type_error(self):
        """Check that we do not get a TypeError when trying
        to query an index with a key that has an invalid type
        """
        index = self._makeOne('counter')

        class Dummy:
            id = 1
            counter = 'test'
        obj = Dummy()
        index.index_object(obj.id, obj)
        query = IndexQuery({'counter': 'test'}, 'counter')
        res = index.query_index(query)
        self.assertListEqual(list(res), [1])
        query = IndexQuery({'counter': None}, 'counter')
        res = index.query_index(query)
        self.assertListEqual(list(res), [])
        query = IndexQuery({'counter': 42}, 'counter')
        res = index.query_index(query)
        self.assertListEqual(list(res), [])

    def test_not(self):
        index = self._makeOne('idx')
        index.query_options = ('not', 'operator')
        apply = index._apply_index
        for i, vals in enumerate(((10, 11, 12), (11, 12, 13))):
            for v in vals:
                index.insertForwardIndexEntry(v, i)
        query = {'query': (10, 11), 'not': (10,)}
        req = dict(idx=query)
        self.assertEqual((1,), tuple(apply(req)[0]), 'or(10,11), not(10)')
        query['operator'] = 'and'
        self.assertEqual((), tuple(apply(req)[0]), 'and(10, 11), not(10)')
        query['query'] = 11
        self.assertEqual((1,), tuple(apply(req)[0]), '11, not(10)')

    def test_range(self):
        index = self._makeOne('idx')
        index.query_options = ('range', 'usage')
        apply = index._apply_index
        docs = tuple(range(10))
        for i in docs:
            index.insertForwardIndexEntry(i, i)
        ranges = ((9, None), (None, 1), (5, 6))
        for op in ('range', 'usage'):
            for r in ranges:
                spec = (['range'] if op == 'usage' else []) + (['min'] if r[0] is not None else []) + (['max'] if r[1] is not None else [])
                query = {'query': [v for v in r if v is not None], op: ':'.join(spec)}
                self.assertEqual(docs[r[0]:r[1] + 1 if r[1] is not None else None], tuple(apply(dict(idx=query))[0]), f'{op}: {r}')