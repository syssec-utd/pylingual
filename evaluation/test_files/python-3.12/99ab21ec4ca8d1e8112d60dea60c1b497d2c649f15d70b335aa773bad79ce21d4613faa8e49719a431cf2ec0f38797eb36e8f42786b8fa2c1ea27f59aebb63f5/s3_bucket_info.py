"""
Copyright (c) 2017 Ansible Project
GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: s3_bucket_info\nversion_added: 1.0.0\nauthor:\n  - "Gerben Geijteman (@hyperized)"\nshort_description: Lists S3 buckets in AWS\ndescription:\n  - Lists S3 buckets and details about those buckets.\n  - Prior to release 5.0.0 this module was called C(community.aws.aws_s3_bucket_info).\n    The usage did not change.\noptions:\n  name:\n    description:\n      - Name of bucket to query.\n    type: str\n    default: ""\n    version_added: 1.4.0\n  name_filter:\n    description:\n      - Limits buckets to only buckets who\'s name contain the string in I(name_filter).\n    type: str\n    default: ""\n    version_added: 1.4.0\n  bucket_facts:\n    description:\n      - Retrieve requested S3 bucket detailed information.\n      - Each bucket_X option executes one API call, hence many options being set to C(true) will cause slower module execution.\n      - You can limit buckets by using the I(name) or I(name_filter) option.\n    suboptions:\n      bucket_accelerate_configuration:\n        description: Retrive S3 accelerate configuration.\n        type: bool\n        default: False\n      bucket_location:\n        description: Retrive S3 bucket location.\n        type: bool\n        default: False\n      bucket_replication:\n        description: Retrive S3 bucket replication.\n        type: bool\n        default: False\n      bucket_acl:\n        description: Retrive S3 bucket ACLs.\n        type: bool\n        default: False\n      bucket_logging:\n        description: Retrive S3 bucket logging.\n        type: bool\n        default: False\n      bucket_request_payment:\n        description: Retrive S3 bucket request payment.\n        type: bool\n        default: False\n      bucket_tagging:\n        description: Retrive S3 bucket tagging.\n        type: bool\n        default: False\n      bucket_cors:\n        description: Retrive S3 bucket CORS configuration.\n        type: bool\n        default: False\n      bucket_notification_configuration:\n        description: Retrive S3 bucket notification configuration.\n        type: bool\n        default: False\n      bucket_encryption:\n        description: Retrive S3 bucket encryption.\n        type: bool\n        default: False\n      bucket_ownership_controls:\n        description:\n        - Retrive S3 ownership controls.\n        type: bool\n        default: False\n      bucket_website:\n        description: Retrive S3 bucket website.\n        type: bool\n        default: False\n      bucket_policy:\n        description: Retrive S3 bucket policy.\n        type: bool\n        default: False\n      bucket_policy_status:\n        description: Retrive S3 bucket policy status.\n        type: bool\n        default: False\n      bucket_lifecycle_configuration:\n        description: Retrive S3 bucket lifecycle configuration.\n        type: bool\n        default: False\n      public_access_block:\n        description: Retrive S3 bucket public access block.\n        type: bool\n        default: False\n    type: dict\n    version_added: 1.4.0\n  transform_location:\n    description:\n      - S3 bucket location for default us-east-1 is normally reported as C(null).\n      - Setting this option to C(true) will return C(us-east-1) instead.\n      - Affects only queries with I(bucket_facts=true) and I(bucket_location=true).\n    type: bool\n    default: False\n    version_added: 1.4.0\nextends_documentation_fragment:\n  - amazon.aws.aws\n  - amazon.aws.ec2\n  - amazon.aws.boto3\n'
EXAMPLES = '\n# Note: These examples do not set authentication details, see the AWS Guide for details.\n\n# Note: Only AWS S3 is currently supported\n\n# Lists all S3 buckets\n- community.aws.s3_bucket_info:\n  register: result\n\n# Retrieve detailed bucket information\n- community.aws.s3_bucket_info:\n    # Show only buckets with name matching\n    name_filter: your.testing\n    # Choose facts to retrieve\n    bucket_facts:\n      # bucket_accelerate_configuration: true\n      bucket_acl: true\n      bucket_cors: true\n      bucket_encryption: true\n      # bucket_lifecycle_configuration: true\n      bucket_location: true\n      # bucket_logging: true\n      # bucket_notification_configuration: true\n      # bucket_ownership_controls: true\n      # bucket_policy: true\n      # bucket_policy_status: true\n      # bucket_replication: true\n      # bucket_request_payment: true\n      # bucket_tagging: true\n      # bucket_website: true\n      # public_access_block: true\n    transform_location: true\n    register: result\n\n# Print out result\n- name: List buckets\n  ansible.builtin.debug:\n    msg: "{{ result[\'buckets\'] }}"\n'
RETURN = '\nbucket_list:\n  description: "List of buckets"\n  returned: always\n  type: complex\n  contains:\n    name:\n      description: Bucket name.\n      returned: always\n      type: str\n      sample: a-testing-bucket-name\n    creation_date:\n      description: Bucket creation date timestamp.\n      returned: always\n      type: str\n      sample: "2021-01-21T12:44:10+00:00"\n    public_access_block:\n      description: Bucket public access block configuration.\n      returned: when I(bucket_facts=true) and I(public_access_block=true)\n      type: complex\n      contains:\n        PublicAccessBlockConfiguration:\n          description: PublicAccessBlockConfiguration data.\n          returned: when PublicAccessBlockConfiguration is defined for the bucket\n          type: complex\n          contains:\n            BlockPublicAcls:\n              description: BlockPublicAcls setting value.\n              type: bool\n              sample: true\n            BlockPublicPolicy:\n              description: BlockPublicPolicy setting value.\n              type: bool\n              sample: true\n            IgnorePublicAcls:\n              description: IgnorePublicAcls setting value.\n              type: bool\n              sample: true\n            RestrictPublicBuckets:\n              description: RestrictPublicBuckets setting value.\n              type: bool\n              sample: true\n    bucket_name_filter:\n      description: String used to limit buckets. See I(name_filter).\n      returned: when I(name_filter) is defined\n      type: str\n      sample: filter-by-this-string\n    bucket_acl:\n      description: Bucket ACL configuration.\n      returned: when I(bucket_facts=true) and I(bucket_acl=true)\n      type: complex\n      contains:\n        Grants:\n          description: List of ACL grants.\n          type: list\n          sample: []\n        Owner:\n          description: Bucket owner information.\n          type: complex\n          contains:\n            DisplayName:\n              description: Bucket owner user display name.\n              returned: always\n              type: str\n              sample: username\n            ID:\n              description: Bucket owner user ID.\n              returned: always\n              type: str\n              sample: 123894e509349etc\n    bucket_cors:\n      description: Bucket CORS configuration.\n      returned: when I(bucket_facts=true) and I(bucket_cors=true)\n      type: complex\n      contains:\n        CORSRules:\n          description: Bucket CORS configuration.\n          returned: when CORS rules are defined for the bucket\n          type: list\n          sample: []\n    bucket_encryption:\n      description: Bucket encryption configuration.\n      returned: when I(bucket_facts=true) and I(bucket_encryption=true)\n      type: complex\n      contains:\n        ServerSideEncryptionConfiguration:\n          description: ServerSideEncryptionConfiguration configuration.\n          returned: when encryption is enabled on the bucket\n          type: complex\n          contains:\n            Rules:\n              description: List of applied encryptio rules.\n              returned: when encryption is enabled on the bucket\n              type: list\n              sample: { "ApplyServerSideEncryptionByDefault": { "SSEAlgorithm": "AES256" }, "BucketKeyEnabled": False }\n    bucket_lifecycle_configuration:\n      description: Bucket lifecycle configuration settings.\n      returned: when I(bucket_facts=true) and I(bucket_lifecycle_configuration=true)\n      type: complex\n      contains:\n        Rules:\n          description: List of lifecycle management rules.\n          returned: when lifecycle configuration is present\n          type: list\n          sample: [{ "Status": "Enabled", "ID": "example-rule" }]\n    bucket_location:\n      description: Bucket location.\n      returned: when I(bucket_facts=true) and I(bucket_location=true)\n      type: complex\n      contains:\n        LocationConstraint:\n          description: AWS region.\n          returned: always\n          type: str\n          sample: us-east-2\n    bucket_logging:\n      description: Server access logging configuration.\n      returned: when I(bucket_facts=true) and I(bucket_logging=true)\n      type: complex\n      contains:\n        LoggingEnabled:\n          description: Server access logging configuration.\n          returned: when server access logging is defined for the bucket\n          type: complex\n          contains:\n            TargetBucket:\n              description: Target bucket name.\n              returned: always\n              type: str\n              sample: logging-bucket-name\n            TargetPrefix:\n              description: Prefix in target bucket.\n              returned: always\n              type: str\n              sample: ""\n    bucket_notification_configuration:\n      description: Bucket notification settings.\n      returned: when I(bucket_facts=true) and I(bucket_notification_configuration=true)\n      type: complex\n      contains:\n        TopicConfigurations:\n          description: List of notification events configurations.\n          returned: when at least one notification is configured\n          type: list\n          sample: []\n    bucket_ownership_controls:\n      description: Preffered object ownership settings.\n      returned: when I(bucket_facts=true) and I(bucket_ownership_controls=true)\n      type: complex\n      contains:\n        OwnershipControls:\n          description: Object ownership settings.\n          returned: when ownership controls are defined for the bucket\n          type: complex\n          contains:\n            Rules:\n              description: List of ownership rules.\n              returned: when ownership rule is defined\n              type: list\n              sample: [{ "ObjectOwnership:": "ObjectWriter" }]\n    bucket_policy:\n      description: Bucket policy contents.\n      returned: when I(bucket_facts=true) and I(bucket_policy=true)\n      type: str\n      sample: \'{"Version":"2012-10-17","Statement":[{"Sid":"AddCannedAcl","Effect":"Allow",..}}]}\'\n    bucket_policy_status:\n      description: Status of bucket policy.\n      returned: when I(bucket_facts=true) and I(bucket_policy_status=true)\n      type: complex\n      contains:\n        PolicyStatus:\n          description: Status of bucket policy.\n          returned: when bucket policy is present\n          type: complex\n          contains:\n            IsPublic:\n              description: Report bucket policy public status.\n              returned: when bucket policy is present\n              type: bool\n              sample: True\n    bucket_replication:\n      description: Replication configuration settings.\n      returned: when I(bucket_facts=true) and I(bucket_replication=true)\n      type: complex\n      contains:\n        Role:\n          description: IAM role used for replication.\n          returned: when replication rule is defined\n          type: str\n          sample: "arn:aws:iam::123:role/example-role"\n        Rules:\n          description: List of replication rules.\n          returned: when replication rule is defined\n          type: list\n          sample: [{ "ID": "rule-1", "Filter": "{}" }]\n    bucket_request_payment:\n      description: Requester pays setting.\n      returned: when I(bucket_facts=true) and I(bucket_request_payment=true)\n      type: complex\n      contains:\n        Payer:\n          description: Current payer.\n          returned: always\n          type: str\n          sample: BucketOwner\n    bucket_tagging:\n      description: Bucket tags.\n      returned: when I(bucket_facts=true) and I(bucket_tagging=true)\n      type: dict\n      sample: { "Tag1": "Value1", "Tag2": "Value2" }\n    bucket_website:\n      description: Static website hosting.\n      returned: when I(bucket_facts=true) and I(bucket_website=true)\n      type: complex\n      contains:\n        ErrorDocument:\n          description: Object serving as HTTP error page.\n          returned: when static website hosting is enabled\n          type: dict\n          sample: { "Key": "error.html" }\n        IndexDocument:\n          description: Object serving as HTTP index page.\n          returned: when static website hosting is enabled\n          type: dict\n          sample: { "Suffix": "error.html" }\n        RedirectAllRequestsTo:\n          description: Website redict settings.\n          returned: when redirect requests is configured\n          type: complex\n          contains:\n            HostName:\n              description: Hostname to redirect.\n              returned: always\n              type: str\n              sample: www.example.com\n            Protocol:\n              description: Protocol used for redirect.\n              returned: always\n              type: str\n              sample: https\n'
try:
    import botocore
except ImportError:
    pass
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import boto3_tag_list_to_ansible_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict

def get_bucket_list(module, connection, name='', name_filter=''):
    """
    Return result of list_buckets json encoded
    Filter only buckets matching 'name' or name_filter if defined
    :param module:
    :param connection:
    :return:
    """
    buckets = []
    filtered_buckets = []
    final_buckets = []
    try:
        buckets = camel_dict_to_snake_dict(connection.list_buckets())['buckets']
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as err_code:
        module.fail_json_aws(err_code, msg='Failed to list buckets')
    if name_filter:
        for bucket in buckets:
            if name_filter in bucket['name']:
                filtered_buckets.append(bucket)
    elif name:
        for bucket in buckets:
            if name == bucket['name']:
                filtered_buckets.append(bucket)
    if name or name_filter:
        final_buckets = filtered_buckets
    else:
        final_buckets = buckets
    return final_buckets

def get_buckets_facts(connection, buckets, requested_facts, transform_location):
    """
    Retrive additional information about S3 buckets
    """
    full_bucket_list = []
    for bucket in buckets:
        bucket.update(get_bucket_details(connection, bucket['name'], requested_facts, transform_location))
        full_bucket_list.append(bucket)
    return full_bucket_list

def get_bucket_details(connection, name, requested_facts, transform_location):
    """
    Execute all enabled S3API get calls for selected bucket
    """
    all_facts = {}
    for key in requested_facts:
        if requested_facts[key]:
            if key == 'bucket_location':
                all_facts[key] = {}
                try:
                    all_facts[key] = get_bucket_location(name, connection, transform_location)
                except botocore.exceptions.ClientError:
                    pass
            elif key == 'bucket_tagging':
                all_facts[key] = {}
                try:
                    all_facts[key] = get_bucket_tagging(name, connection)
                except botocore.exceptions.ClientError:
                    pass
            else:
                all_facts[key] = {}
                try:
                    all_facts[key] = get_bucket_property(name, connection, key)
                except botocore.exceptions.ClientError:
                    pass
    return all_facts

@AWSRetry.jittered_backoff(max_delay=120, catch_extra_error_codes=['NoSuchBucket', 'OperationAborted'])
def get_bucket_location(name, connection, transform_location=False):
    """
    Get bucket location and optionally transform 'null' to 'us-east-1'
    """
    data = connection.get_bucket_location(Bucket=name)
    if transform_location:
        try:
            if not data['LocationConstraint']:
                data['LocationConstraint'] = 'us-east-1'
        except KeyError:
            pass
    data.pop('ResponseMetadata', None)
    return data

@AWSRetry.jittered_backoff(max_delay=120, catch_extra_error_codes=['NoSuchBucket', 'OperationAborted'])
def get_bucket_tagging(name, connection):
    """
    Get bucket tags and transform them using `boto3_tag_list_to_ansible_dict` function
    """
    data = connection.get_bucket_tagging(Bucket=name)
    try:
        bucket_tags = boto3_tag_list_to_ansible_dict(data['TagSet'])
        return bucket_tags
    except KeyError:
        data.pop('ResponseMetadata', None)
        return data

@AWSRetry.jittered_backoff(max_delay=120, catch_extra_error_codes=['NoSuchBucket', 'OperationAborted'])
def get_bucket_property(name, connection, get_api_name):
    """
    Get bucket property
    """
    api_call = 'get_' + get_api_name
    api_function = getattr(connection, api_call)
    data = api_function(Bucket=name)
    data.pop('ResponseMetadata', None)
    return data

def main():
    """
    Get list of S3 buckets
    :return:
    """
    argument_spec = dict(name=dict(type='str', default=''), name_filter=dict(type='str', default=''), bucket_facts=dict(type='dict', options=dict(bucket_accelerate_configuration=dict(type='bool', default=False), bucket_acl=dict(type='bool', default=False), bucket_cors=dict(type='bool', default=False), bucket_encryption=dict(type='bool', default=False), bucket_lifecycle_configuration=dict(type='bool', default=False), bucket_location=dict(type='bool', default=False), bucket_logging=dict(type='bool', default=False), bucket_notification_configuration=dict(type='bool', default=False), bucket_ownership_controls=dict(type='bool', default=False), bucket_policy=dict(type='bool', default=False), bucket_policy_status=dict(type='bool', default=False), bucket_replication=dict(type='bool', default=False), bucket_request_payment=dict(type='bool', default=False), bucket_tagging=dict(type='bool', default=False), bucket_website=dict(type='bool', default=False), public_access_block=dict(type='bool', default=False))), transform_location=dict(type='bool', default=False))
    result = {}
    mutually_exclusive = [['name', 'name_filter']]
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=mutually_exclusive)
    name = module.params.get('name')
    name_filter = module.params.get('name_filter')
    requested_facts = module.params.get('bucket_facts')
    transform_location = module.params.get('bucket_facts')
    connection = {}
    try:
        connection = module.client('s3')
    except (connection.exceptions.ClientError, botocore.exceptions.BotoCoreError) as err_code:
        module.fail_json_aws(err_code, msg='Failed to connect to AWS')
    bucket_list = get_bucket_list(module, connection, name, name_filter)
    if name:
        result['bucket_name'] = name
    elif name_filter:
        result['bucket_name_filter'] = name_filter
    bucket_facts = module.params.get('bucket_facts')
    if bucket_facts:
        result['buckets'] = get_buckets_facts(connection, bucket_list, requested_facts, transform_location)
    else:
        result['buckets'] = bucket_list
    module.exit_json(msg='Retrieved s3 info.', **result)
if __name__ == '__main__':
    main()