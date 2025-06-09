from test_helper import exchange_updates
import pytest
from y_py import YDoc, YArray, YArrayEvent
from copy import deepcopy
import json

def test_inserts():
    d1 = YDoc(1)
    x = d1.get_array('test')
    with d1.begin_transaction() as txn:
        x.insert_range(txn, 0, [1, 2.5, 'hello', ['world'], True])
    with d1.begin_transaction() as txn:
        x.extend(txn, [{'key': 'value'}])
    expected = [1, 2.5, 'hello', ['world'], True, {'key': 'value'}]
    assert list(x) == expected
    d2 = YDoc(2)
    x = d2.get_array('test')
    exchange_updates([d1, d2])
    assert list(x) == expected

def test_to_string():
    arr = YArray([7, 'awesome', True, ['nested'], {'testing': 'dicts'}])
    expected_str = "[7, 'awesome', True, ['nested'], {'testing': 'dicts'}]"
    assert str(arr) == expected_str
    assert arr.__repr__() == f'YArray({expected_str})'

def test_to_json():
    contents = [7, 'awesome', True, ['nested'], {'testing': 'dicts'}]
    doc = YDoc()
    prelim = YArray(deepcopy(contents))
    integrated = doc.get_array('arr')
    with doc.begin_transaction() as txn:
        integrated.extend(txn, contents)
    expected_json = '[7,"awesome",true,["nested"],{"testing":"dicts"}]'
    assert integrated.to_json() == expected_json
    assert prelim.to_json() == expected_json
    assert json.loads(integrated.to_json()) == contents

def test_inserts_nested():
    d1 = YDoc()
    x = d1.get_array('test')
    to_list = lambda arr: [list(x) if type(x) == YArray else x for x in arr]
    nested = YArray()
    d1.transact(lambda txn: nested.append(txn, 'world'))
    d1.transact(lambda txn: x.insert_range(txn, 0, [1, 2, nested, 3, 4]))
    d1.transact(lambda txn: nested.insert(txn, 0, 'hello'))
    expected = [1, 2, ['hello', 'world'], 3, 4]
    assert type(x[2]) == YArray
    assert to_list(x) == expected
    d2 = YDoc()
    x = d2.get_array('test')
    exchange_updates([d1, d2])
    assert to_list(x) == expected

def test_delete():
    d1 = YDoc(1)
    assert d1.client_id == 1
    x = d1.get_array('test')
    d1.transact(lambda txn: x.insert_range(txn, 0, [1, 2, ['hello', 'world'], {'user': 'unknown'}, "I'm here too!", True]))
    d1.transact(lambda txn: x.delete_range(txn, 1, 3))
    expected = [1, "I'm here too!", True]
    assert list(x) == expected
    with d1.begin_transaction() as txn:
        x.delete(txn, 1)
    assert list(x) == [1.0, True]
    with pytest.raises(IndexError):
        with d1.begin_transaction() as txn:
            x.delete(txn, 2)
    d2 = YDoc(2)
    x = d2.get_array('test')
    exchange_updates([d1, d2])
    assert list(x) == [1.0, True]

def test_get():
    d1 = YDoc()
    integrated = d1.get_array('test')
    prelim = YArray()
    d1.transact(lambda txn: integrated.insert_range(txn, 0, [1, 2, True]))
    d1.transact(lambda txn: integrated.insert_range(txn, 1, ['hello', 'world']))
    expected = [1, 'hello', 'world', 2, True]
    prelim = YArray(expected)
    for arr in [integrated, prelim]:
        for (i, expected_value) in enumerate(expected):
            assert arr[i] == expected_value
        with pytest.raises(IndexError):
            arr[5]
        for (i, expected_value) in enumerate(reversed(expected)):
            index = -(i + 1)
            assert arr[index] == expected_value
        with pytest.raises(IndexError):
            arr[-6]
        assert arr[0:] == expected
        assert arr[4:1:-1] == expected[4:1:-1]
        assert arr[::-1] == expected[::-1]

def test_iterator():
    d1 = YDoc()
    x = d1.get_array('test')
    with d1.begin_transaction() as txn:
        x.insert_range(txn, 0, [1, 2, 3])
    assert len(x) == 3
    i = 1.0
    for v in x:
        assert v == i
        i += 1.0
    assert 2.0 in x

def test_borrow_mut_edge_case():
    """
    Tests for incorrect overlap in successive mutable borrows of YTransaction and YArray.
    """
    doc = YDoc()
    arr = doc.get_array('test')
    with doc.begin_transaction() as txn:
        arr.insert_range(txn, 0, [1, 2, 3])
    with doc.begin_transaction() as txn:
        for i in range(2000):
            arr.insert_range(txn, 2, [1, 2, 3])
            arr.delete_range(txn, 0, 3)

def test_observer():
    d1 = YDoc()
    x = d1.get_array('test')
    target = None
    delta = None

    def callback(e: YArrayEvent):
        nonlocal target
        nonlocal delta
        target = e.target
        delta = e.delta
    subscription_id = x.observe(callback)
    with d1.begin_transaction() as txn:
        x.insert_range(txn, 0, [1, 2, 3, 4])
    assert list(target) == list(x)
    assert delta == [{'insert': [1, 2, 3, 4]}]
    target = None
    delta = None
    with d1.begin_transaction() as txn:
        x.delete_range(txn, 1, 2)
    assert list(target) == list(x)
    assert delta == [{'retain': 1}, {'delete': 2}]
    target = None
    delta = None
    with d1.begin_transaction() as txn:
        x.insert(txn, 1, 5)
    assert list(target) == list(x)
    assert delta == [{'retain': 1}, {'insert': [5]}]
    target = None
    delta = None
    x.unobserve(subscription_id)
    with d1.begin_transaction() as txn:
        x.insert(txn, 1, 6)
    assert target == None
    assert delta == None

def test_deep_observe():
    """
    Ensure that changes to elements inside the array trigger a callback.
    """
    ydoc = YDoc()
    container = ydoc.get_array('container')
    yarray = YArray([1, 2])
    with ydoc.begin_transaction() as txn:
        container.append(txn, yarray)
    events = None

    def callback(e: list):
        nonlocal events
        events = e
    sub = container.observe_deep(callback)
    with ydoc.begin_transaction() as txn:
        container[0].append(txn, 3)
    assert events != None
    events = None
    container.unobserve(sub)
    with ydoc.begin_transaction() as txn:
        container[0].append(txn, 4)
    assert events == None

def test_move_to():
    """
    Ensure that move_to works.
    """
    doc = YDoc()
    arr = doc.get_array('test')
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_to(t, 0, 10))
    assert list(arr) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_to(t, 9, 0))
    assert list(arr) == [9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_to(t, 6, 5))
    assert list(arr) == [0, 1, 2, 3, 4, 6, 5, 7, 8, 9]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    with pytest.raises(Exception):
        doc.transact(lambda t: arr.move_to(t, -1, 5))
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    with pytest.raises(Exception):
        doc.transact(lambda t: arr.move_to(t, 0, -5))

def test_move_range_to():
    """
    Ensure that move_range_to works.
    """
    doc = YDoc()
    arr = doc.get_array('test')
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3])
    doc.transact(lambda t: arr.move_range_to(t, 1, 2, 4))
    assert list(arr) == [0, 3, 1, 2]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 0, 0, 10))
    assert list(arr) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 0, 1, 10))
    assert list(arr) == [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 3, 5, 7))
    assert list(arr) == [0, 1, 2, 6, 3, 4, 5, 7, 8, 9]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 1, 0, 10))
    assert list(arr) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 3, 5, 5))
    assert list(arr) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 9, 9, 0))
    assert list(arr) == [9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 8, 9, 0))
    assert list(arr) == [8, 9, 0, 1, 2, 3, 4, 5, 6, 7]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 4, 6, 3))
    assert list(arr) == [0, 1, 2, 4, 5, 6, 3, 7, 8, 9]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    doc.transact(lambda t: arr.move_range_to(t, 3, 5, 3))
    assert list(arr) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    with pytest.raises(Exception):
        doc.transact(lambda t: arr.move_range_to(t, -1, 2, 5))
    with doc.begin_transaction() as t:
        arr.delete_range(t, 0, len(arr))
        arr.extend(t, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    with pytest.raises(Exception):
        doc.transact(lambda t: arr.move_range_to(t, 0, -1, 3))