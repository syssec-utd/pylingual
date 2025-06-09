from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: s3_website\nversion_added: 1.0.0\nshort_description: Configure an s3 bucket as a website\ndescription:\n    - Configure an s3 bucket as a website\nauthor: Rob White (@wimnat)\noptions:\n  name:\n    description:\n      - "Name of the s3 bucket"\n    required: true\n    type: str\n  error_key:\n    description:\n      - "The object key name to use when a 4XX class error occurs. To remove an error key, set to None."\n    type: str\n  redirect_all_requests:\n    description:\n      - "Describes the redirect behavior for every request to this s3 bucket website endpoint"\n    type: str\n  state:\n    description:\n      - "Add or remove s3 website configuration"\n    choices: [ \'present\', \'absent\' ]\n    required: true\n    type: str\n  suffix:\n    description:\n      - >\n        Suffix that is appended to a request that is for a directory on the website endpoint (e.g. if the suffix is index.html and you make a request to\n        samplebucket/images/ the data that is returned will be for the object with the key name images/index.html). The suffix must not include a slash\n        character.\n    default: index.html\n    type: str\n\nextends_documentation_fragment:\n- amazon.aws.aws\n- amazon.aws.ec2\n- amazon.aws.boto3\n\n'
EXAMPLES = '\n# Note: These examples do not set authentication details, see the AWS Guide for details.\n\n- name: Configure an s3 bucket to redirect all requests to example.com\n  community.aws.s3_website:\n    name: mybucket.com\n    redirect_all_requests: example.com\n    state: present\n\n- name: Remove website configuration from an s3 bucket\n  community.aws.s3_website:\n    name: mybucket.com\n    state: absent\n\n- name: Configure an s3 bucket as a website with index and error pages\n  community.aws.s3_website:\n    name: mybucket.com\n    suffix: home.htm\n    error_key: errors/404.htm\n    state: present\n\n'
RETURN = '\nindex_document:\n    description: index document\n    type: complex\n    returned: always\n    contains:\n        suffix:\n            description: suffix that is appended to a request that is for a directory on the website endpoint\n            returned: success\n            type: str\n            sample: index.html\nerror_document:\n    description: error document\n    type: complex\n    returned: always\n    contains:\n        key:\n            description:  object key name to use when a 4XX class error occurs\n            returned: when error_document parameter set\n            type: str\n            sample: error.html\nredirect_all_requests_to:\n    description: where to redirect requests\n    type: complex\n    returned: always\n    contains:\n        host_name:\n            description: name of the host where requests will be redirected.\n            returned: when redirect all requests parameter set\n            type: str\n            sample: ansible.com\n        protocol:\n            description: protocol to use when redirecting requests.\n            returned: when redirect all requests parameter set\n            type: str\n            sample: https\nrouting_rules:\n    description: routing rules\n    type: list\n    returned: always\n    contains:\n        condition:\n            type: complex\n            description: A container for describing a condition that must be met for the specified redirect to apply.\n            contains:\n                http_error_code_returned_equals:\n                    description: The HTTP error code when the redirect is applied.\n                    returned: always\n                    type: str\n                key_prefix_equals:\n                    description: object key name prefix when the redirect is applied. For example, to redirect\n                                 requests for ExamplePage.html, the key prefix will be ExamplePage.html\n                    returned: when routing rule present\n                    type: str\n                    sample: docs/\n        redirect:\n            type: complex\n            description: Container for redirect information.\n            returned: always\n            contains:\n                host_name:\n                    description: name of the host where requests will be redirected.\n                    returned: when host name set as part of redirect rule\n                    type: str\n                    sample: ansible.com\n                http_redirect_code:\n                    description: The HTTP redirect code to use on the response.\n                    returned: when routing rule present\n                    type: str\n                protocol:\n                    description: Protocol to use when redirecting requests.\n                    returned: when routing rule present\n                    type: str\n                    sample: http\n                replace_key_prefix_with:\n                    description: object key prefix to use in the redirect request\n                    returned: when routing rule present\n                    type: str\n                    sample: documents/\n                replace_key_with:\n                    description: object key prefix to use in the redirect request\n                    returned: when routing rule present\n                    type: str\n                    sample: documents/\n'
import time
try:
    import botocore
except ImportError:
    pass
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.core import is_boto3_error_code

def _create_redirect_dict(url):
    redirect_dict = {}
    url_split = url.split(':')
    if len(url_split) == 2:
        redirect_dict[u'Protocol'] = url_split[0]
        redirect_dict[u'HostName'] = url_split[1].replace('//', '')
    elif len(url_split) == 1:
        redirect_dict[u'HostName'] = url_split[0]
    else:
        raise ValueError('Redirect URL appears invalid')
    return redirect_dict

def _create_website_configuration(suffix, error_key, redirect_all_requests):
    website_configuration = {}
    if error_key is not None:
        website_configuration['ErrorDocument'] = {'Key': error_key}
    if suffix is not None:
        website_configuration['IndexDocument'] = {'Suffix': suffix}
    if redirect_all_requests is not None:
        website_configuration['RedirectAllRequestsTo'] = _create_redirect_dict(redirect_all_requests)
    return website_configuration

def enable_or_update_bucket_as_website(client_connection, resource_connection, module):
    bucket_name = module.params.get('name')
    redirect_all_requests = module.params.get('redirect_all_requests')
    if redirect_all_requests is not None:
        suffix = None
    else:
        suffix = module.params.get('suffix')
    error_key = module.params.get('error_key')
    changed = False
    try:
        bucket_website = resource_connection.BucketWebsite(bucket_name)
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to get bucket')
    try:
        website_config = client_connection.get_bucket_website(Bucket=bucket_name)
    except is_boto3_error_code('NoSuchWebsiteConfiguration'):
        website_config = None
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to get website configuration')
    if website_config is None:
        try:
            bucket_website.put(WebsiteConfiguration=_create_website_configuration(suffix, error_key, redirect_all_requests))
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Failed to set bucket website configuration')
        except ValueError as e:
            module.fail_json(msg=str(e))
    else:
        try:
            if suffix is not None and website_config['IndexDocument']['Suffix'] != suffix or (error_key is not None and website_config['ErrorDocument']['Key'] != error_key) or (redirect_all_requests is not None and website_config['RedirectAllRequestsTo'] != _create_redirect_dict(redirect_all_requests)):
                try:
                    bucket_website.put(WebsiteConfiguration=_create_website_configuration(suffix, error_key, redirect_all_requests))
                    changed = True
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    module.fail_json_aws(e, msg='Failed to update bucket website configuration')
        except KeyError as e:
            try:
                bucket_website.put(WebsiteConfiguration=_create_website_configuration(suffix, error_key, redirect_all_requests))
                changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg='Failed to update bucket website configuration')
        except ValueError as e:
            module.fail_json(msg=str(e))
        time.sleep(5)
    website_config = client_connection.get_bucket_website(Bucket=bucket_name)
    module.exit_json(changed=changed, **camel_dict_to_snake_dict(website_config))

def disable_bucket_as_website(client_connection, module):
    changed = False
    bucket_name = module.params.get('name')
    try:
        client_connection.get_bucket_website(Bucket=bucket_name)
    except is_boto3_error_code('NoSuchWebsiteConfiguration'):
        module.exit_json(changed=changed)
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to get bucket website')
    try:
        client_connection.delete_bucket_website(Bucket=bucket_name)
        changed = True
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to delete bucket website')
    module.exit_json(changed=changed)

def main():
    argument_spec = dict(name=dict(type='str', required=True), state=dict(type='str', required=True, choices=['present', 'absent']), suffix=dict(type='str', required=False, default='index.html'), error_key=dict(type='str', required=False, no_log=False), redirect_all_requests=dict(type='str', required=False))
    module = AnsibleAWSModule(argument_spec=argument_spec, mutually_exclusive=[['redirect_all_requests', 'suffix'], ['redirect_all_requests', 'error_key']])
    try:
        client_connection = module.client('s3')
        resource_connection = module.resource('s3')
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to connect to AWS')
    state = module.params.get('state')
    if state == 'present':
        enable_or_update_bucket_as_website(client_connection, resource_connection, module)
    elif state == 'absent':
        disable_bucket_as_website(client_connection, module)
if __name__ == '__main__':
    main()