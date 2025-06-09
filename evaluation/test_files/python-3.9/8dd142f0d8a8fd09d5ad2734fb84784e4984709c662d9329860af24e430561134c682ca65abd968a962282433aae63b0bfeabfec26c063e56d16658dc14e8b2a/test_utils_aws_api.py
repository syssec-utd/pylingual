import boto3
import pytest
from moto import mock_ec2, mock_iam, mock_route53
from reconcile.utils.aws_api import AmiTag, AWSApi

@pytest.fixture
def accounts():
    return [{'name': 'some-account', 'automationToken': {'path': 'path'}, 'resourcesDefaultRegion': 'default-region'}]

@pytest.fixture
def aws_api(accounts, mocker):
    mock_secret_reader = mocker.patch('reconcile.utils.aws_api.SecretReader', autospec=True)
    mock_secret_reader.return_value.read_all.return_value = {'aws_access_key_id': 'key_id', 'aws_secret_access_key': 'access_key', 'region': 'tf_state_bucket_region'}
    return AWSApi(1, accounts, init_users=False)

@pytest.fixture
def iam_client():
    with mock_iam():
        iam_client = boto3.client('iam')
        yield iam_client

def test_get_user_key_list(aws_api, iam_client):
    iam_client.create_user(UserName='user')
    iam_client.create_access_key(UserName='user')
    key_list = aws_api._get_user_key_list(iam_client, 'user')
    assert key_list != []

def test_get_user_key_list_empty(aws_api, iam_client):
    iam_client.create_user(UserName='user')
    key_list = aws_api._get_user_key_list(iam_client, 'user')
    assert key_list == []

def test_get_user_key_list_missing_user(aws_api, iam_client):
    iam_client.create_user(UserName='user1')
    key_list = aws_api._get_user_key_list(iam_client, 'user2')
    assert key_list == []

def test_get_user_keys(aws_api, iam_client):
    iam_client.create_user(UserName='user')
    iam_client.create_access_key(UserName='user')
    keys = aws_api.get_user_keys(iam_client, 'user')
    assert keys != []

def test_get_user_keys_empty(aws_api, iam_client):
    iam_client.create_user(UserName='user')
    keys = aws_api.get_user_keys(iam_client, 'user')
    assert keys == []

def test_get_user_key_status(aws_api, iam_client):
    iam_client.create_user(UserName='user')
    iam_client.create_access_key(UserName='user')
    key = aws_api.get_user_keys(iam_client, 'user')[0]
    status = aws_api.get_user_key_status(iam_client, 'user', key)
    assert status == 'Active'

def test_default_region(aws_api, accounts):
    for a in accounts:
        assert aws_api.sessions[a['name']].region_name == a['resourcesDefaultRegion']

def test_filter_amis_regex(aws_api):
    regex = '^match.*$'
    images = [{'Name': 'match-regex', 'ImageId': 'id1', 'State': 'available', 'Tags': []}, {'Name': 'no-match-regex', 'ImageId': 'id2', 'State': 'available', 'Tags': []}]
    results = aws_api._filter_amis(images, regex)
    expected = {'image_id': 'id1', 'tags': []}
    assert results == [expected]

def test_filter_amis_state(aws_api):
    regex = '^match.*$'
    images = [{'Name': 'match-regex-1', 'ImageId': 'id1', 'State': 'available', 'Tags': []}, {'Name': 'match-regex-2', 'ImageId': 'id2', 'State': 'pending', 'Tags': []}]
    results = aws_api._filter_amis(images, regex)
    expected = {'image_id': 'id1', 'tags': []}
    assert results == [expected]

@pytest.fixture
def route53_client():
    with mock_route53():
        route53_client = boto3.client('route53')
        yield route53_client

def test_get_hosted_zone_id(aws_api):
    zone_id = 'THISISTHEZONEID'
    zone = {'Id': f'/hostedzone/{zone_id}'}
    result = aws_api._get_hosted_zone_id(zone)
    assert result == zone_id

def test_get_hosted_zone_record_sets_empty(aws_api, route53_client):
    zone_name = 'test.example.com.'
    results = aws_api._get_hosted_zone_record_sets(route53_client, zone_name)
    assert results == []

def test_get_hosted_zone_record_sets_exists(aws_api, route53_client):
    zone_name = 'test.example.com.'
    route53_client.create_hosted_zone(Name=zone_name, CallerReference='test')
    zones = route53_client.list_hosted_zones_by_name(DNSName=zone_name)['HostedZones']
    zone_id = aws_api._get_hosted_zone_id(zones[0])
    record_set = {'Name': zone_name, 'Type': 'NS', 'ResourceRecords': [{'Value': 'ns'}]}
    change_batch = {'Changes': [{'Action': 'CREATE', 'ResourceRecordSet': record_set}]}
    route53_client.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
    results = aws_api._get_hosted_zone_record_sets(route53_client, zone_name)
    assert results == [record_set]

def test_filter_record_sets(aws_api):
    zone_name = 'a'
    record_type = 'NS'
    expected = {'Name': f'{zone_name}.', 'Type': record_type}
    record_sets = [expected, {'Name': f'{zone_name}.', 'Type': 'SOA'}, {'Name': f'not-{zone_name}.', 'Type': record_type}]
    results = aws_api._filter_record_sets(record_sets, zone_name, 'NS')
    assert results == [expected]

def test_extract_records(aws_api):
    record = 'ns.example.com'
    resource_records = [{'Value': f'{record}.'}]
    results = aws_api._extract_records(resource_records)
    assert results == [record]

@pytest.fixture
def ec2_client():
    with mock_ec2():
        yield boto3.client('ec2', region_name='us-east-1')

def test_get_image_id(ec2_client, aws_api: AWSApi):
    reservation = ec2_client.run_instances(ImageId='ami-bb9a6bc2', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    ec2_client.create_image(InstanceId=instance_id, Name='image-1')
    ami_x86_64 = ec2_client.create_image(InstanceId=instance_id, Name='x86_64', TagSpecifications=[{'ResourceType': 'image', 'Tags': [{'Key': 'foo', 'Value': 'bar'}, {'Key': 'commit', 'Value': 'sha-123456'}, {'Key': 'arch', 'Value': 'x86_64'}]}])['ImageId']
    ami_aarch64 = ec2_client.create_image(InstanceId=instance_id, Name='aarch64', TagSpecifications=[{'ResourceType': 'image', 'Tags': [{'Key': 'foo', 'Value': 'bar'}, {'Key': 'commit', 'Value': 'sha-123456'}, {'Key': 'arch', 'Value': 'aarch64'}]}])['ImageId']
    assert aws_api.get_image_id('some-account', 'us-east-1', tags=[AmiTag(name='arch', value='x86_64')]) == ami_x86_64
    assert aws_api.get_image_id('some-account', 'us-east-1', tags=[AmiTag(name='commit', value='sha-123456'), AmiTag(name='arch', value='aarch64')]) == ami_aarch64
    with pytest.raises(ValueError):
        aws_api.get_image_id('some-account', 'us-east-1', tags=[AmiTag(name='foo', value='bar')])