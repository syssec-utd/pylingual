from time import sleep
from unittest import TestCase
from unittest.mock import patch
from pollect.core.config.ConfigContainer import ConfigContainer
from pollect.sources.SnmpGetSource import SnmpGetSource, SnmpValue

class TestSnmpGetSource(TestCase):

    def test_overflow_delta(self):
        value = SnmpValue(SnmpValue.COUNTER32, 0)
        self.assertEqual(1, value.get_delta(4294967295))
        value = SnmpValue(SnmpValue.COUNTER32, 5)
        self.assertEqual(6, value.get_delta(4294967295))
        value = SnmpValue(SnmpValue.COUNTER32, 5)
        self.assertEqual(4, value.get_delta(1))

    @patch('pollect.sources.SnmpGetSource.subprocess.check_output')
    def test_simple(self, mock_check_output):
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.48 = Counter32: 123'
        mock_check_output.return_value = std_out.encode('utf-8')
        source = SnmpGetSource({'host': '10.1.1.1', 'metrics': [{'oid': 'iso.3.6.1.2.1.16.1.1.1.3.48', 'name': 'Test'}], 'type': '-'})
        data = source.probe()[0]
        self.assertEqual(1, len(data.values))
        self.assertEqual(123, data.values[0].value)

    @patch('pollect.sources.SnmpGetSource.subprocess.check_output')
    def test_simple_with_label(self, mock_check_output):
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.48 = Counter32: 123\niso.3.6.1.2.1.31.1.1.1.123 = STRING: "sample"'
        mock_check_output.return_value = std_out.encode('utf-8')
        source = SnmpGetSource(ConfigContainer({'host': '10.1.1.1', 'metrics': [{'oid': 'iso.3.6.1.2.1.16.1.1.1.3.48', 'oidLabels': {'paramName': 'iso.3.6.1.2.1.31.1.1.1.123'}, 'name': 'Test'}], 'type': '-'}))
        data = source.probe()[0]
        self.assertEqual(1, len(data.labels))
        self.assertEqual('paramName', data.labels[0])
        self.assertEqual(1, len(data.values))
        self.assertEqual('sample', data.values[0].label_values[0])
        self.assertEqual(123, data.values[0].value)

    @patch('pollect.sources.SnmpGetSource.subprocess.check_output')
    def test_range(self, mock_check_output):
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.1 = Counter32: 123\niso.3.6.1.2.1.16.1.1.1.3.2 = Counter32: 10\niso.3.6.1.2.1.16.1.1.1.3.3 = Counter32: 11\n'
        mock_check_output.return_value = std_out.encode('utf-8')
        config = ConfigContainer({'host': '10.1.1.1', 'metrics': [{'oid': 'iso.3.6.1.2.1.16.1.1.1.3.${randomParam}', 'range': {'from': 1, 'to': 3, 'label': 'randomParam'}, 'name': 'Test'}], 'type': '-'})
        source = SnmpGetSource(config)
        data = source.probe()[0]
        self.assertEqual(3, len(data.values))
        self.assertEqual('Test', data.values[0].name)
        self.assertEqual('Test', data.values[1].name)
        self.assertEqual('Test', data.values[2].name)
        self.assertEqual('randomParam', data.labels[0])
        self.assertEqual('1', data.values[0].label_values[0])
        self.assertEqual('2', data.values[1].label_values[0])
        self.assertEqual('3', data.values[2].label_values[0])
        self.assertEqual(123, data.values[0].value)
        self.assertEqual(10, data.values[1].value)
        self.assertEqual(11, data.values[2].value)

    @patch('pollect.sources.SnmpGetSource.subprocess.check_output')
    def test_range_with_labels(self, mock_check_output):
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.1 = Counter32: 123\niso.3.6.1.2.1.16.1.1.1.3.2 = Counter32: 10\niso.3.6.1.2.1.16.1.1.1.3.3 = Counter32: 11\niso.3.6.1.2.1.50.1.1.1.3.1 = Counter32: 11\n\niso.3.6.1.2.1.31.1.1.1.18.1 = STRING: "test name1"\niso.3.6.1.2.1.31.1.1.1.18.2 = STRING: "test name2"\niso.3.6.1.2.1.31.1.1.1.18.3 = STRING: "test name3"\n'
        mock_check_output.return_value = std_out.encode('utf-8')
        config = ConfigContainer({'host': '10.1.1.1', 'metrics': [{'oid': 'iso.3.6.1.2.1.16.1.1.1.3.${randomParam}', 'oidLabels': {'portName': 'iso.3.6.1.2.1.31.1.1.1.18.${randomParam}'}, 'range': {'from': 1, 'to': 3, 'label': 'randomParam'}, 'name': 'Test'}, {'oid': 'iso.3.6.1.2.1.50.1.1.1.3.${randomParam}', 'oidLabels': {'portName': 'iso.3.6.1.2.1.31.1.1.1.18.${randomParam}'}, 'range': {'from': 1, 'to': 3, 'label': 'randomParam'}, 'name': 'Test'}], 'type': '-'})
        source = SnmpGetSource(config)
        result = source.probe()
        data = result[0]
        self.assertEqual(3, len(data.values))
        self.assertEqual('Test', data.values[0].name)
        self.assertEqual('Test', data.values[1].name)
        self.assertEqual('Test', data.values[2].name)
        self.assertEqual('randomParam', data.labels[0])
        self.assertEqual('portName', data.labels[1])
        self.assertEqual('1', data.values[0].label_values[0])
        self.assertEqual('2', data.values[1].label_values[0])
        self.assertEqual('3', data.values[2].label_values[0])
        self.assertEqual('test name1', data.values[0].label_values[1])
        self.assertEqual('test name2', data.values[1].label_values[1])
        self.assertEqual('test name3', data.values[2].label_values[1])
        self.assertEqual(123, data.values[0].value)
        self.assertEqual(10, data.values[1].value)
        self.assertEqual(11, data.values[2].value)
        data = result[1]
        self.assertEqual(1, len(data.values))
        self.assertEqual('Test', data.values[0].name)
        self.assertEqual('randomParam', data.labels[0])
        self.assertEqual('portName', data.labels[1])
        self.assertEqual('1', data.values[0].label_values[0])
        self.assertEqual('test name1', data.values[0].label_values[1])
        self.assertEqual(11, data.values[0].value)

    @patch('pollect.sources.SnmpGetSource.subprocess.check_output')
    def test_rate(self, mock_check_output):
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.48 = Counter32: 0'
        mock_check_output.return_value = std_out.encode('utf-8')
        source = SnmpGetSource({'host': '10.1.1.1', 'metrics': [{'oid': 'iso.3.6.1.2.1.16.1.1.1.3.48', 'name': 'Test', 'mode': 'rate'}], 'type': '-'})
        data = source.probe()[0]
        self.assertEqual(0, len(data.values))
        sleep(1)
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.48 = Counter32: 10'
        mock_check_output.return_value = std_out.encode('utf-8')
        data = source.probe()[0]
        self.assertEqual(1, len(data.values))
        self.assertAlmostEqual(10, data.values[0].value, 0)

    @patch('pollect.sources.SnmpGetSource.subprocess.check_output')
    def test_rate_overflow(self, mock_check_output):
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.48 = Counter32: 4294967290'
        mock_check_output.return_value = std_out.encode('utf-8')
        source = SnmpGetSource({'host': '10.1.1.1', 'metrics': [{'oid': 'iso.3.6.1.2.1.16.1.1.1.3.48', 'name': 'Test', 'mode': 'rate'}], 'type': '-'})
        data = source.probe()[0]
        self.assertEqual(0, len(data.values))
        sleep(1)
        std_out = 'iso.3.6.1.2.1.16.1.1.1.3.48 = Counter32: 10'
        mock_check_output.return_value = std_out.encode('utf-8')
        data = source.probe()[0]
        self.assertEqual(1, len(data.values))
        self.assertAlmostEqual(16, data.values[0].value, 0)