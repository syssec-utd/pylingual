import unittest
import logging
import sys
import os
from unittest.mock import patch, Mock
import graphsignal
from graphsignal.endpoint_trace import EndpointTrace
logger = logging.getLogger('graphsignal')

class GraphsignalTest(unittest.TestCase):

    def setUp(self):
        if len(logger.handlers) == 0:
            logger.addHandler(logging.StreamHandler(sys.stdout))
        graphsignal.configure(api_key='k1', deployment='d1', upload_on_shutdown=False, debug_mode=True)

    def tearDown(self):
        graphsignal.shutdown()

    def test_check_and_set_arg_test(self):
        arg1 = graphsignal._check_and_set_arg('arg1', 'val1', is_str=True, required=True)
        self.assertEqual(arg1, 'val1')
        arg2 = graphsignal._check_and_set_arg('arg2', 1, is_int=True, required=True)
        self.assertEqual(arg2, 1)
        arg3 = graphsignal._check_and_set_arg('arg3', None, is_int=True, required=False)
        self.assertEqual(arg3, None)
        os.environ['GRAPHSIGNAL_ARG4'] = '2'
        arg4 = graphsignal._check_and_set_arg('arg4', None, is_int=True, required=False)
        self.assertEqual(arg4, 2)
        with self.assertRaises(ValueError):
            arg5 = graphsignal._check_and_set_arg('arg5', None, is_str=True, required=True)
        os.environ['GRAPHSIGNAL_ARG6'] = '10'
        arg6 = graphsignal._check_and_set_arg('arg6', None, is_int=True, required=True)
        self.assertEqual(arg6, 10)
        os.environ['GRAPHSIGNAL_ARG7'] = 'str'
        with self.assertRaises(ValueError):
            arg7 = graphsignal._check_and_set_arg('arg7', None, is_int=True, required=True)
        os.environ['GRAPHSIGNAL_ARG8'] = 'a=1, b = c '
        arg8 = graphsignal._check_and_set_arg('arg8', None, is_kv=True, required=True)
        self.assertEqual(arg8, {'a': '1', 'b': 'c'})
        os.environ['GRAPHSIGNAL_ARG9'] = 'a'
        with self.assertRaises(ValueError):
            arg9 = graphsignal._check_and_set_arg('arg9', None, is_kv=True, required=False)

    def test_configure(self):
        self.assertIsNotNone(graphsignal._agent.worker_id)
        self.assertEqual(graphsignal._agent.api_key, 'k1')
        self.assertEqual(graphsignal._agent.debug_mode, True)

    @patch.object(EndpointTrace, '_stop', return_value=None)
    @patch.object(EndpointTrace, '_start', return_value=None)
    def test_trace_function(self, mocked_start, mocked_stop):

        @graphsignal.trace_function
        def test_func(p):
            return 1 + p
        ret = test_func(12)
        self.assertEqual(ret, 13)
        mocked_start.assert_called_once()
        mocked_stop.assert_called_once()

    @patch.object(EndpointTrace, '_stop', return_value=None)
    @patch.object(EndpointTrace, '_start', return_value=None)
    def test_trace_function_with_args(self, mocked_start, mocked_stop):

        @graphsignal.trace_function(endpoint='ep1', tags=dict(t1='v1'))
        def test_func(p):
            return 1 + p
        ret = test_func(12)
        self.assertEqual(ret, 13)
        mocked_start.assert_called_once()
        mocked_stop.assert_called_once()