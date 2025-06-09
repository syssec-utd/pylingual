import os
import sys
import six
import json
import tccli.options_define as OptionsDefine
import tccli.format_output as FormatOutput
from tccli import __version__
from tccli.utils import Utils
from tccli.exceptions import ConfigurationError, ClientError, ParamError
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.yinsuda.v20220527 import yinsuda_client as yinsuda_client_v20220527
from tencentcloud.yinsuda.v20220527 import models as models_v20220527
from jmespath import search
import time

def doCreateKTVRobot(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CreateKTVRobotRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.CreateKTVRobot(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doSyncKTVRobotCommand(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.SyncKTVRobotCommandRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.SyncKTVRobotCommand(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVTags(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVTagsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVTags(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doApplyChorus(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ApplyChorusRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.ApplyChorus(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVPlaylistDetail(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVPlaylistDetailRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVPlaylistDetail(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDestroyKTVRobot(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DestroyKTVRobotRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DestroyKTVRobot(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVMatchMusics(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVMatchMusicsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVMatchMusics(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVSuggestions(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVSuggestionsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVSuggestions(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeUserInfo(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeUserInfoRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeUserInfo(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doBatchDescribeKTVMusicDetails(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.BatchDescribeKTVMusicDetailsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.BatchDescribeKTVMusicDetails(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVPlaylists(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVPlaylistsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVPlaylists(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doRechargeLiveVip(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.RechargeLiveVipRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.RechargeLiveVip(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeLiveVipTradeInfos(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeLiveVipTradeInfosRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeLiveVipTradeInfos(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVRobots(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVRobotsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVRobots(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doSearchKTVMusics(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.SearchKTVMusicsRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.SearchKTVMusics(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])

def doDescribeKTVMusicsByTag(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)
    if g_param[OptionsDefine.UseCVMRole.replace('-', '_')]:
        cred = credential.CVMRoleCredential()
    elif g_param[OptionsDefine.RoleArn.replace('-', '_')] and g_param[OptionsDefine.RoleSessionName.replace('-', '_')]:
        cred = credential.STSAssumeRoleCredential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.RoleArn.replace('-', '_')], g_param[OptionsDefine.RoleSessionName.replace('-', '_')])
    elif os.getenv(OptionsDefine.ENV_TKE_REGION) and os.getenv(OptionsDefine.ENV_TKE_PROVIDER_ID) and os.getenv(OptionsDefine.ENV_TKE_IDENTITY_TOKEN_FILE) and os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN):
        cred = credential.DefaultTkeOIDCRoleArnProvider().get_credentials()
    else:
        cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token])
    http_profile = HttpProfile(reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]), reqMethod='POST', endpoint=g_param[OptionsDefine.Endpoint], proxy=g_param[OptionsDefine.HttpsProxy.replace('-', '_')])
    profile = ClientProfile(httpProfile=http_profile, signMethod='HmacSHA256')
    if g_param[OptionsDefine.Language]:
        profile.language = g_param[OptionsDefine.Language]
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.YinsudaClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += '_CLI_' + __version__
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeKTVMusicsByTagRequest()
    model.from_json_string(json.dumps(args))
    start_time = time.time()
    while True:
        rsp = client.DescribeKTVMusicsByTag(model)
        result = rsp.to_json_string()
        try:
            json_obj = json.loads(result)
        except TypeError as e:
            json_obj = json.loads(result.decode('utf-8'))
        if not g_param[OptionsDefine.Waiter] or search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj) == g_param['OptionsDefine.WaiterInfo']['to']:
            break
        cur_time = time.time()
        if cur_time - start_time >= g_param['OptionsDefine.WaiterInfo']['timeout']:
            raise ClientError('Request timeout, wait `%s` to `%s` timeout, last request is %s' % (g_param['OptionsDefine.WaiterInfo']['expr'], g_param['OptionsDefine.WaiterInfo']['to'], search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj)))
        else:
            print('Inquiry result is %s.' % search(g_param['OptionsDefine.WaiterInfo']['expr'], json_obj))
        time.sleep(g_param['OptionsDefine.WaiterInfo']['interval'])
    FormatOutput.output('action', json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])
CLIENT_MAP = {'v20220527': yinsuda_client_v20220527}
MODELS_MAP = {'v20220527': models_v20220527}
ACTION_MAP = {'CreateKTVRobot': doCreateKTVRobot, 'SyncKTVRobotCommand': doSyncKTVRobotCommand, 'DescribeKTVTags': doDescribeKTVTags, 'ApplyChorus': doApplyChorus, 'DescribeKTVPlaylistDetail': doDescribeKTVPlaylistDetail, 'DestroyKTVRobot': doDestroyKTVRobot, 'DescribeKTVMatchMusics': doDescribeKTVMatchMusics, 'DescribeKTVSuggestions': doDescribeKTVSuggestions, 'DescribeUserInfo': doDescribeUserInfo, 'BatchDescribeKTVMusicDetails': doBatchDescribeKTVMusicDetails, 'DescribeKTVPlaylists': doDescribeKTVPlaylists, 'RechargeLiveVip': doRechargeLiveVip, 'DescribeLiveVipTradeInfos': doDescribeLiveVipTradeInfos, 'DescribeKTVRobots': doDescribeKTVRobots, 'SearchKTVMusics': doSearchKTVMusics, 'DescribeKTVMusicsByTag': doDescribeKTVMusicsByTag}
AVAILABLE_VERSION_LIST = ['v20220527']

def action_caller():
    return ACTION_MAP

def parse_global_arg(parsed_globals):
    g_param = parsed_globals
    is_exist_profile = True
    if not parsed_globals['profile']:
        is_exist_profile = False
        g_param['profile'] = 'default'
    configure_path = os.path.join(os.path.expanduser('~'), '.tccli')
    (is_conf_exist, conf_path) = Utils.file_existed(configure_path, g_param['profile'] + '.configure')
    (is_cred_exist, cred_path) = Utils.file_existed(configure_path, g_param['profile'] + '.credential')
    conf = {}
    cred = {}
    if is_conf_exist:
        conf = Utils.load_json_msg(conf_path)
    if is_cred_exist:
        cred = Utils.load_json_msg(cred_path)
    if not (isinstance(conf, dict) and isinstance(cred, dict)):
        raise ConfigurationError('file: %s or %s is not json format' % (g_param['profile'] + '.configure', g_param['profile'] + '.credential'))
    if OptionsDefine.Token not in cred:
        cred[OptionsDefine.Token] = None
    if not is_exist_profile:
        if os.environ.get(OptionsDefine.ENV_SECRET_ID) and os.environ.get(OptionsDefine.ENV_SECRET_KEY):
            cred[OptionsDefine.SecretId] = os.environ.get(OptionsDefine.ENV_SECRET_ID)
            cred[OptionsDefine.SecretKey] = os.environ.get(OptionsDefine.ENV_SECRET_KEY)
            cred[OptionsDefine.Token] = os.environ.get(OptionsDefine.ENV_TOKEN)
        if os.environ.get(OptionsDefine.ENV_REGION):
            conf[OptionsDefine.Region] = os.environ.get(OptionsDefine.ENV_REGION)
        if os.environ.get(OptionsDefine.ENV_ROLE_ARN) and os.environ.get(OptionsDefine.ENV_ROLE_SESSION_NAME):
            cred[OptionsDefine.RoleArn] = os.environ.get(OptionsDefine.ENV_ROLE_ARN)
            cred[OptionsDefine.RoleSessionName] = os.environ.get(OptionsDefine.ENV_ROLE_SESSION_NAME)
    for param in g_param.keys():
        if g_param[param] is None:
            if param in [OptionsDefine.SecretKey, OptionsDefine.SecretId, OptionsDefine.Token]:
                if param in cred:
                    g_param[param] = cred[param]
                elif not (g_param[OptionsDefine.UseCVMRole.replace('-', '_')] or os.getenv(OptionsDefine.ENV_TKE_ROLE_ARN)):
                    raise ConfigurationError('%s is invalid' % param)
            elif param in [OptionsDefine.Region, OptionsDefine.Output, OptionsDefine.Language]:
                if param in conf:
                    g_param[param] = conf[param]
                elif param != OptionsDefine.Language:
                    raise ConfigurationError('%s is invalid' % param)
            elif param.replace('_', '-') in [OptionsDefine.RoleArn, OptionsDefine.RoleSessionName]:
                if param.replace('_', '-') in cred:
                    g_param[param] = cred[param.replace('_', '-')]
    try:
        if g_param[OptionsDefine.ServiceVersion]:
            g_param[OptionsDefine.Version] = 'v' + g_param[OptionsDefine.ServiceVersion].replace('-', '')
        else:
            version = conf['yinsuda'][OptionsDefine.Version]
            g_param[OptionsDefine.Version] = 'v' + version.replace('-', '')
        if g_param[OptionsDefine.Endpoint] is None:
            g_param[OptionsDefine.Endpoint] = conf['yinsuda'][OptionsDefine.Endpoint]
    except Exception as err:
        raise ConfigurationError('config file:%s error, %s' % (conf_path, str(err)))
    if g_param[OptionsDefine.Version] not in AVAILABLE_VERSION_LIST:
        raise Exception('available versions: %s' % ' '.join(AVAILABLE_VERSION_LIST))
    if g_param[OptionsDefine.Waiter]:
        param = eval(g_param[OptionsDefine.Waiter])
        if 'expr' not in param:
            raise Exception('`expr` in `--waiter` must be defined')
        if 'to' not in param:
            raise Exception('`to` in `--waiter` must be defined')
        if 'timeout' not in param:
            if 'waiter' in conf and 'timeout' in conf['waiter']:
                param['timeout'] = conf['waiter']['timeout']
            else:
                param['timeout'] = 180
        if 'interval' not in param:
            if 'waiter' in conf and 'interval' in conf['waiter']:
                param['interval'] = conf['waiter']['interval']
            else:
                param['interval'] = 5
        param['interval'] = min(param['interval'], param['timeout'])
        g_param['OptionsDefine.WaiterInfo'] = param
    if six.PY2:
        for (key, value) in g_param.items():
            if isinstance(value, six.text_type):
                g_param[key] = value.encode('utf-8')
    return g_param