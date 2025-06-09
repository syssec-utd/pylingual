import mock
import pytest
import requests
from mock import patch
import os
from cogniceptshell.common import bcolors
from cogniceptshell.configuration import Configuration

class SuccessAwsCredentials(object):

    def __init__(self):
        self.status_code = 200

    def json(self):
        return {'AccessKeyId': os.getenv('AWS_ACCESS_KEY_ID', ''), 'SecretAccessKey': os.getenv('AWS_SECRET_ACCESS_KEY', ''), 'SessionToken': ''}

class NotFoundMockResponse(object):

    def __init__(self):
        self.status_code = 404

def mock_aws_endpoint(*args, **kwargs):
    if args[0] == 'https://test.cognicept.systems/api/agent/v1/aws/assume_role':
        return SuccessAwsCredentials()
    else:
        return NotFoundMockResponse()

def setup_file(tmpdir):
    p = tmpdir.join('runtime.env')
    p.write('COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2\nCOGNICEPT_API_URI=https://test.cognicept.systems/api/agent/v1/aws/assume_role\nCOGNICEPT_ACCESS_KEY=CORRECT-KEY')

def setup_wrong_uri_file(tmpdir):
    p = tmpdir.join('runtime.env')
    p.write('COGNICEPT_API_URI=https://www.wronguri.blame\nCOGNICEPT_ACCESS_KEY=INCORRECT-KEY')

def setup_correct_uri_file(tmpdir):
    p = tmpdir.join('runtime.env')
    p.write('COGNICEPT_API_URI=https://test.cognicept.systems/api/agent/v1/\nCOGNICEPT_ACCESS_KEY=CORRECT-KEY')

def setup_wrong_uri_file_for_init(tmpdir):
    p = tmpdir.join('runtime.env')

def setup_correct_uri_file_for_init(tmpdir):
    p = tmpdir.join('runtime.env')
    p.write('COGNICEPT_USER_API_URI=https://test.cognicept.systems/api/agent/v1/')

def mock_shutil_copy_fail_no_space(arg1, arg2):
    test_exp = OSError(28, 'No space left on device')
    raise test_exp

def mock_shutil_copy_fail_others(arg1, arg2):
    test_exp = OSError(1, 'Operation not permitted')
    raise test_exp

def mock_shutil_copy_success(arg1, arg2):
    pass

def mock_file_write_fail(arg1, arg2):
    raise PermissionError

def test_yes_input():
    object = Configuration()
    assert object._interpret_bool_input('Y') == True

def test_no_input():
    object = Configuration()
    assert object._interpret_bool_input('n') == False

def test_other_input():
    object = Configuration()
    assert object._interpret_bool_input('g') == None
    assert object._interpret_bool_input('%') == None
    assert object._interpret_bool_input('1') == None
    assert object._interpret_bool_input('akjflakjewr4f56f74ew@!!@$@!$') == None

def test_is_ssh_disabled(tmpdir):
    setup_file(tmpdir)
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    assert object.is_ssh_enabled() == False
    object.config['COG_ENABLE_SSH_KEY_AUTH'] = False
    assert object.is_ssh_enabled() == False

def test_is_ssh_disabled(tmpdir):
    setup_file(tmpdir)
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    object.config['COG_ENABLE_SSH_KEY_AUTH'] = True
    assert object.is_ssh_enabled() == True

def test_incorrect_cognicept_key_fetch_aws_keys(tmpdir, capsys, monkeypatch):
    setup_wrong_uri_file(tmpdir)
    monkeypatch.setattr(requests, 'get', mock_aws_endpoint)
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    try:
        result = object.fetch_aws_keys()
        assert result == False
    except:
        pytest.fail('Incorrect Cognicept API URI gave exception', pytrace=True)

def test_correct_cognicept_key_fetch_aws_keys(tmpdir, capsys, monkeypatch):
    setup_correct_uri_file(tmpdir)
    monkeypatch.setattr(requests, 'get', mock_aws_endpoint)
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    try:
        result = object.fetch_aws_keys()
        assert result == SuccessAwsCredentials().json()
    except:
        pytest.fail('Correct Cognicept API URI gave exception', pytrace=True)

def test_wrong_get_cognicept_api_uri_init(tmpdir, capsys):
    setup_wrong_uri_file_for_init(tmpdir)
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    result = object.get_cognicept_user_api_uri()
    assert result == 'https://app.cognicept.systems/api/v1/'

def test_correct_get_cognicept_api_uri_init(tmpdir, capsys):
    setup_correct_uri_file_for_init(tmpdir)
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    result = object.get_cognicept_user_api_uri()
    assert result == 'https://test.cognicept.systems/api/agent/v1/'

def test_no_runtime_dotenv(tmpdir, capsys):
    object = Configuration()
    object.load_config(str(tmpdir) + '/')
    captured = capsys.readouterr()
    assert str(captured.out) == 'Configuration file `' + str(tmpdir) + '/runtime.env` does not exist.\nConfiguration file `' + str(tmpdir) + '/runtime.env` is empty or could not be parsed.\n'

def test_with_runtime_dotenv(tmpdir, capsys):
    setup_file(tmpdir)
    object = Configuration()
    result = object.load_config(str(tmpdir) + '/')
    assert result == True

def test_save_config_success(tmpdir, capsys):
    setup_file(tmpdir)
    object = Configuration()
    result = object.load_config(str(tmpdir) + '/')
    object.save_config()
    captured = capsys.readouterr()
    assert str(captured.out) == bcolors.OKBLUE + 'Backed up runtime configuration to: ' + str(tmpdir) + '/runtime.env.bk' + bcolors.ENDC + '\n'

def test_save_config_fail_backup_no_space(tmpdir, capsys):
    setup_file(tmpdir)
    object = Configuration()
    result = object.load_config(str(tmpdir) + '/')
    with patch('shutil.copyfile', new=mock_shutil_copy_fail_no_space):
        object.save_config()
        captured = capsys.readouterr()
    assert str(captured.out) == bcolors.FAIL + 'Could not back up runtime configuration. Aborting saving runtime configuration. No space left on device!' + bcolors.ENDC + '\n'

def test_save_config_fail_backup_other_exceptions(tmpdir, capsys):
    setup_file(tmpdir)
    object = Configuration()
    result = object.load_config(str(tmpdir) + '/')
    with patch('shutil.copyfile', new=mock_shutil_copy_fail_others):
        object.save_config()
        captured = capsys.readouterr()
    assert str(captured.out) == bcolors.FAIL + 'Could not back up runtime configuration. Aborting saving runtime configuration: Operation not permitted' + bcolors.ENDC + '\n'

def test_save_config_fail_permissions(tmpdir, capsys):
    setup_file(tmpdir)
    object = Configuration()
    result = object.load_config(str(tmpdir) + '/')
    with patch('shutil.copyfile', new=mock_shutil_copy_success):
        with mock.patch('builtins.open', mock_file_write_fail):
            object.save_config()
            captured = capsys.readouterr()
    assert str(captured.out) == bcolors.OKBLUE + 'Backed up runtime configuration to: ' + str(tmpdir) + '/runtime.env.bk' + bcolors.ENDC + '\n' + bcolors.FAIL + 'Could not write into `' + str(tmpdir) + '/runtime.env' + '`. Please check write permission or run with `sudo`.' + bcolors.ENDC + '\n'

def test_get_docker_compose(monkeypatch):
    object = Configuration()
    object.config = {'COG_COMPOSE_FILE': '/path/to/docker-compose.yml'}
    yaml_data = '\n    services:\n        camera_top:\n            image: 412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/ros:realsense\n        ip_cam_front:\n            image: 412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/ros:crystal\n    '
    mock_file = mock.mock_open(read_data=yaml_data)
    monkeypatch.setattr('builtins.open', mock_file)
    result = object.get_docker_compose()
    expected_result = {'camera_top': '412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/ros:realsense', 'ip_cam_front': '412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/ros:crystal'}
    assert result == expected_result

def test_fail_get_docker_compose_(monkeypatch, capsys):
    object = Configuration()
    object.config = {'COG_COMPOSE_FILE': '/path/to/docker-compose.yml'}
    result = object.get_docker_compose()
    assert result == {}
    yaml_data = ''
    mock_file = mock.mock_open(read_data=yaml_data)
    monkeypatch.setattr('builtins.open', mock_file)
    result = object.get_docker_compose()
    assert result == {}
    yaml_data = '\n    services:\n    camera_top:\n            image: 412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/ros:realsense\n        ip_cam_front:\n            image: 412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/ros:crystal\n    '
    mock_file1 = mock.mock_open(read_data=yaml_data)
    monkeypatch.setattr('builtins.open', mock_file1)
    result = object.get_docker_compose()
    assert result == {}