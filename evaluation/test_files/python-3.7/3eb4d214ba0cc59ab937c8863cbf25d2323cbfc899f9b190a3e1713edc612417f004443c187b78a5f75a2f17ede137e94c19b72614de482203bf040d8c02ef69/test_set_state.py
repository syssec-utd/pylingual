import pytest
from unittest import mock
from traitlets import Bool, Tuple, List, Instance, CFloat, CInt, Float, Int, TraitError, observe
from .utils import setup, teardown
import ipywidgets
from ipywidgets import Widget

@pytest.fixture(params=[True, False])
def echo(request):
    oldvalue = ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO
    ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO = request.param
    yield request.param
    ipywidgets.widgets.widget.JUPYTER_WIDGETS_ECHO = oldvalue

class SimpleWidget(Widget):
    a = Bool().tag(sync=True)
    b = Tuple(Bool(), Bool(), Bool(), default_value=(False, False, False)).tag(sync=True)
    c = List(Bool()).tag(sync=True)

class NumberWidget(Widget):
    f = Float().tag(sync=True)
    cf = CFloat().tag(sync=True)
    i = Int().tag(sync=True)
    ci = CInt().tag(sync=True)

def transform_fromjson(data, widget):
    if not data[0]:
        return data
    return [False] + data[1:-2] + [data[-1], data[-2]]

class TransformerWidget(Widget):
    d = List(Bool()).tag(sync=True, from_json=transform_fromjson)

class DataInstance:

    def __init__(self, data=None):
        self.data = data

def mview_serializer(instance, widget):
    return {'data': memoryview(instance.data) if instance.data else None}

def bytes_serializer(instance, widget):
    return {'data': bytearray(memoryview(instance.data).tobytes()) if instance.data else None}

def deserializer(json_data, widget):
    return DataInstance(memoryview(json_data['data']).tobytes() if json_data else None)

class DataWidget(SimpleWidget):
    d = Instance(DataInstance, args=()).tag(sync=True, to_json=mview_serializer, from_json=deserializer)

def truncate_deserializer(json_data, widget):
    return DataInstance(json_data['data'][:20].tobytes() if json_data else None)

class TruncateDataWidget(SimpleWidget):
    d = Instance(DataInstance, args=()).tag(sync=True, to_json=bytes_serializer, from_json=truncate_deserializer)

def test_set_state_simple(echo):
    w = SimpleWidget()
    w.set_state(dict(a=True, b=[True, False, True], c=[False, True, False]))
    assert len(w.comm.messages) == (1 if echo else 0)

def test_set_state_transformer(echo):
    w = TransformerWidget()
    w.set_state(dict(d=[True, False, True]))
    expected = []
    if echo:
        expected.append(((), dict(buffers=[], data=dict(buffer_paths=[], method='echo_update', state=dict(d=[True, False, True])))))
    expected.append(((), dict(buffers=[], data=dict(buffer_paths=[], method='update', state=dict(d=[False, True, False])))))
    assert w.comm.messages == expected

def test_set_state_data(echo):
    w = DataWidget()
    data = memoryview(b'x' * 30)
    w.set_state(dict(a=True, d={'data': data}))
    assert len(w.comm.messages) == (1 if echo else 0)

def test_set_state_data_truncate(echo):
    w = TruncateDataWidget()
    data = memoryview(b'x' * 30)
    w.set_state(dict(a=True, d={'data': data}))
    assert len(w.comm.messages) == 2 if echo else 1
    msg = w.comm.messages[-1]
    buffers = msg[1].pop('buffers')
    assert msg == ((), dict(data=dict(method='update', state=dict(d={}), buffer_paths=[['d', 'data']])))
    assert len(buffers) == 1
    assert buffers[0] == data[:20].tobytes()

def test_set_state_numbers_int(echo):
    w = NumberWidget()
    w.set_state(dict(f=1, cf=2, i=3, ci=4))
    assert len(w.comm.messages) == (1 if echo else 0)

def test_set_state_numbers_float(echo):
    w = NumberWidget()
    w.set_state(dict(f=1.0, cf=2.0, ci=4.0))
    assert len(w.comm.messages) == (1 if echo else 0)

def test_set_state_float_to_float(echo):
    w = NumberWidget()
    w.set_state(dict(f=1.2, cf=2.6))
    assert len(w.comm.messages) == (1 if echo else 0)

def test_set_state_cint_to_float(echo):
    w = NumberWidget()
    w.set_state(dict(ci=5.6))
    assert len(w.comm.messages) == (2 if echo else 1)
    msg = w.comm.messages[-1]
    data = msg[1]['data']
    assert data['method'] == 'update'
    assert data['state'] == {'ci': 5}

def _x_test_set_state_int_to_int_like():
    w = NumberWidget()
    w.set_state(dict(i=3.0))
    assert len(w.comm.messages) == 0

def test_set_state_int_to_float(echo):
    w = NumberWidget()
    with pytest.raises(TraitError):
        w.set_state(dict(i=3.5))

def test_property_lock(echo):

    class AnnoyingWidget(Widget):
        value = Float().tag(sync=True)
        stop = Bool(False)

        @observe('value')
        def _propagate_value(self, change):
            print('_propagate_value', change.new)
            if self.stop:
                return
            if change.new == 42:
                self.value = 2
            if change.new == 2:
                self.stop = True
                self.value = 42
    widget = AnnoyingWidget(value=1)
    assert widget.value == 1
    widget._send = mock.MagicMock()
    widget.set_state({'value': 42})
    assert widget.value == 42
    assert widget.stop is True
    calls = []
    widget._send.assert_has_calls(calls)

def test_hold_sync(echo):

    class AnnoyingWidget(Widget):
        value = Float().tag(sync=True)
        other = Float().tag(sync=True)

        @observe('value')
        def _propagate_value(self, change):
            print('_propagate_value', change.new)
            if change.new == 42:
                self.value = 2
                self.other = 11
    widget = AnnoyingWidget(value=1)
    assert widget.value == 1
    widget._send = mock.MagicMock()
    widget.set_state({'value': 42})
    assert widget.value == 2
    assert widget.other == 11
    msg = {'method': 'echo_update', 'state': {'value': 42.0}, 'buffer_paths': []}
    call42 = mock.call(msg, buffers=[])
    msg = {'method': 'update', 'state': {'value': 2.0}, 'buffer_paths': []}
    call2 = mock.call(msg, buffers=[])
    msg = {'method': 'update', 'state': {'other': 11.0}, 'buffer_paths': []}
    call11 = mock.call(msg, buffers=[])
    calls = [call42, call2, call11] if echo else [call2, call11]
    widget._send.assert_has_calls(calls)

def test_echo():

    class ValueWidget(Widget):
        value = Float().tag(sync=True)
    widget = ValueWidget(value=1)
    assert widget.value == 1
    widget._send = mock.MagicMock()
    widget.set_state({'value': 42, 'unexpected_field': 43})
    assert widget.value == 42
    msg = {'method': 'echo_update', 'state': {'value': 42.0}, 'buffer_paths': []}
    call42 = mock.call(msg, buffers=[])
    calls = [call42]
    widget._send.assert_has_calls(calls)

def test_echo_single():

    class ValueWidget(Widget):
        value = Float().tag(sync=True)
        square = Float().tag(sync=True)

        @observe('value')
        def _square(self, change):
            self.square = self.value ** 2
    widget = ValueWidget(value=1)
    assert widget.value == 1
    widget._send = mock.MagicMock()
    widget._handle_msg({'content': {'data': {'method': 'update', 'state': {'value': 8}}}})
    assert widget.value == 8
    assert widget.square == 64
    msg = {'method': 'echo_update', 'state': {'value': 8.0}, 'buffer_paths': []}
    call = mock.call(msg, buffers=[])
    msg = {'method': 'update', 'state': {'square': 64}, 'buffer_paths': []}
    call2 = mock.call(msg, buffers=[])
    calls = [call, call2]
    widget._send.assert_has_calls(calls)

def test_no_echo(echo):

    class ValueWidget(Widget):
        value = Float().tag(sync=True, echo_update=False)
    widget = ValueWidget(value=1)
    assert widget.value == 1
    widget._send = mock.MagicMock()
    widget._handle_msg({'content': {'data': {'method': 'update', 'state': {'value': 42}}}})
    assert widget.value == 42
    widget._send.assert_not_called()
    widget.value = 43
    widget._send.assert_has_calls([mock.call({'method': 'update', 'state': {'value': 43.0}, 'buffer_paths': []}, buffers=[])])