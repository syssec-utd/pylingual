import json
import sys
import xmlrpc.client
from lavacli import main

def test_results_job(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testjob_results_yaml', 'args': ('1234',), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == 'Results:\n* lava.validate [pass]\n* lava.job [fail]\n'

def test_results_job_isatty(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234'])
    monkeypatch.setattr(sys.stdout, 'isatty', lambda : True)
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testjob_results_yaml', 'args': ('1234',), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"}, {"suite": "lava", "name": "boot", "result": "skip"}, {"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == 'Results:\n* lava.validate [\x1b[1;32mpass\x1b[0m]\n* lava.boot [skip]\n* lava.job [\x1b[1;31mfail\x1b[0m]\n'

def test_results_job_json(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', '--json'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testjob_results_yaml', 'args': ('1234',), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert json.loads(capsys.readouterr()[0]) == [{'name': 'validate', 'result': 'pass', 'suite': 'lava'}, {'name': 'job', 'result': 'fail', 'suite': 'lava'}]

def test_results_job_yaml(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', '--yaml'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testjob_results_yaml', 'args': ('1234',), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == '- {name: validate, result: pass, suite: lava}\n- {name: job, result: fail, suite: lava}\n'

def test_results_suite(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testsuite_results_yaml', 'args': ('1234', 'lava'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == 'Results:\n* lava.validate [pass]\n* lava.job [fail]\n'

def test_results_suite_json(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', '--json'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testsuite_results_yaml', 'args': ('1234', 'lava'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert json.loads(capsys.readouterr()[0]) == [{'name': 'validate', 'result': 'pass', 'suite': 'lava'}, {'name': 'job', 'result': 'fail', 'suite': 'lava'}]

def test_results_suite_yaml(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', '--yaml'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testsuite_results_yaml', 'args': ('1234', 'lava'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "job", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == '- {name: validate, result: pass, suite: lava}\n- {name: job, result: fail, suite: lava}\n'

def test_results_case(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == 'pass\n'

def test_results_case_isatty_pass(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate'])
    monkeypatch.setattr(sys.stdout, 'isatty', lambda : True)
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == '\x1b[1;32mpass\x1b[0m\n'

def test_results_case_isatty_fail(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate'])
    monkeypatch.setattr(sys.stdout, 'isatty', lambda : True)
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == '\x1b[1;31mfail\x1b[0m\n'

def test_results_case_isatty_skip(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate'])
    monkeypatch.setattr(sys.stdout, 'isatty', lambda : True)
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "skip"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == 'skip\n'

def test_results_case_1(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"},{"suite": "lava", "name": "validate", "result": "fail"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == 'pass\nfail\n'

def test_results_case_json(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate', '--json'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"}]'}])
    assert main() == 0
    assert json.loads(capsys.readouterr()[0]) == [{'name': 'validate', 'result': 'pass', 'suite': 'lava'}]

def test_results_case_yaml(setup, monkeypatch, capsys):
    version = '2019.1'
    monkeypatch.setattr(sys, 'argv', ['lavacli', 'results', '1234', 'lava', 'validate', '--yaml'])
    monkeypatch.setattr(xmlrpc.client.ServerProxy, 'data', [{'request': 'system.version', 'args': (), 'ret': version}, {'request': 'results.get_testcase_results_yaml', 'args': ('1234', 'lava', 'validate'), 'ret': '[{"suite": "lava", "name": "validate", "result": "pass"}]'}])
    assert main() == 0
    assert capsys.readouterr()[0] == '- {name: validate, result: pass, suite: lava}\n'