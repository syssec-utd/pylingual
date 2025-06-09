import os
import time
import json
import hashlib
import logging
import datetime
import uuid
import mimetypes
from functools import partial
from tornado import ioloop
from tornado import gen
from tornado.web import HTTPError
import psutil
from litedfs.data.config import CONFIG
LOG = logging.getLogger(__name__)
BUF_SIZE = 65536

class Servers(object):
    HTTP_SERVER = None
    SERVERS = []
    TORNADO_INSTANCE = None

async def shutdown():
    LOG.info('Stopping Service(%s:%s)', CONFIG['http_host'], CONFIG['http_port'])
    if Servers.HTTP_SERVER:
        Servers.HTTP_SERVER.stop()
        LOG.info('Stop http server!')
    for s in Servers.SERVERS:
        if hasattr(s, 'close'):
            s.close()
        elif hasattr(s, 'stop'):
            s.stop()
        if hasattr(s, 'name'):
            LOG.info('Stop %s server!', s.name)
        else:
            LOG.info('Stop nameless server!')
    await gen.sleep(1)
    LOG.info('Will shutdown ...')
    ioloop.IOLoop.current().stop()

def sig_handler(sig, frame):
    LOG.warning('sig_handler Caught signal: %s', sig)
    ioloop.IOLoop.current().add_callback_from_signal(shutdown)

class Errors(object):
    OK = 'ok'
    errors = {'ServerException': {'name': 'ServerException', 'message': 'server exception'}, 'InvalidParameters': {'name': 'InvalidParameters', 'message': 'invalid parameters'}, 'OperationFailed': {'name': 'OperationFailed', 'message': 'operation failed'}, 'OperationRunning': {'name': 'OperationRunning', 'message': 'operation running'}, 'BlockNotExists': {'name': 'BlockNotExists', 'message': 'block not exists'}, 'ChecksumFailed': {'name': 'ChecksumFailed', 'message': 'checksum failed'}, 'ReplicateBlockFailed': {'name': 'ReplicateBlockFailed', 'message': 'replicate block failed'}}

    @classmethod
    def set_result_error(cls, error_name, result, message=''):
        if error_name in cls.errors:
            result['result'] = error_name
            if message == '':
                result['message'] = cls.errors[error_name]['message']
            else:
                result['message'] = message
        else:
            result['result'] = 'UnknownError'
            result['message'] = 'unknown error'

class Stage(object):
    pending = 'pending'
    running = 'running'
    finished = 'finished'

class Status(object):
    fail = 'fail'
    success = 'success'
    kill = 'kill'
    cancel = 'cancel'
    terminate = 'terminate'

class Signal(object):
    kill = -9
    terminate = -15
    stop = -15
    cancel = -50

class JSONLoadError(Exception):

    def __init__(self, message):
        self.message = message

class MetaNotDictError(Exception):

    def __init__(self, message):
        self.message = message

def file_sha1sum(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def file_md5sum(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as fp:
        while True:
            data = fp.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def bytes_md5sum(b):
    md5 = hashlib.md5()
    md5.update(b)
    return md5.hexdigest()

def splitall(path):
    allparts = []
    while True:
        parts = os.path.split(path)
        if parts[0] == path:
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            if parts[1]:
                allparts.insert(0, parts[1])
    return allparts

def get_workspace_path(create_at, task_id=None, action_name=None):
    result = ''
    date_create_at = datetime.datetime.strptime(create_at, '%Y-%m-%d %H:%M:%S.%f')
    date_directory_name = date_create_at.strftime('%Y-%m-%d')
    if task_id and action_name:
        result = os.path.join(CONFIG['data_path'], 'tmp', 'workspace', date_directory_name, task_id[:2], task_id[2:4], task_id, action_name)
    elif task_id:
        result = os.path.join(CONFIG['data_path'], 'tmp', 'workspace', date_directory_name, task_id[:2], task_id[2:4], task_id)
    else:
        result = os.path.join(CONFIG['data_path'], 'tmp', 'workspace', date_directory_name)
    return result

def init_storage():
    directories = [os.path.join(CONFIG['data_path'], 'files'), os.path.join(CONFIG['data_path'], 'tmp', 'download')]
    for d in directories:
        if not os.path.exists(d) or not os.path.isdir(d):
            os.makedirs(d)

def delete_file(name):
    try:
        dir_path = os.path.join(CONFIG['data_path'], 'files', name[:2], name[2:4])
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            for file in files:
                if file.startswith(name):
                    os.remove(os.path.join(dir_path, file))
            files = os.listdir(dir_path)
            if len(files) == 0:
                os.rmdir(dir_path)
                dir_parent_path = os.path.split(dir_path)[0]
                files = os.listdir(dir_parent_path)
                if len(files) == 0:
                    os.rmdir(dir_parent_path)
    except Exception as e:
        LOG.exception(e)

def delete_block(name, block):
    try:
        dir_path = os.path.join(CONFIG['data_path'], 'files', name[:2], name[2:4])
        file_path = os.path.join(dir_path, '%s_%s.blk' % (name, block))
        tmp_file_path = os.path.join(dir_path, '%s_%s.blk.tmp' % (name, block))
        check_file_path = os.path.join(dir_path, '%s_%s.chk' % (name, block))
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if os.path.exists(check_file_path):
            os.remove(check_file_path)
        files = os.listdir(dir_path)
        if len(files) == 0:
            os.rmdir(dir_path)
            dir_parent_path = os.path.split(dir_path)[0]
            files = os.listdir(dir_parent_path)
            if len(files) == 0:
                os.rmdir(dir_parent_path)
    except Exception as e:
        LOG.exception(e)

def body_producer(boundary, files, params, write):
    if not isinstance(files, dict):
        raise HTTPError('files must be dict')
    if not isinstance(params, dict):
        raise HTTPError('params must be dict')
    boundary_bytes = boundary.encode()
    for file_name in files:
        file = files[file_name]
        file_name_bytes = file_name.encode()
        write(b'--%s\r\n' % (boundary_bytes,))
        write(b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (file_name.encode(), file_name_bytes))
        mtype = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
        write(b'Content-Type: %s\r\n' % (mtype.encode(),))
        write(b'\r\n')
        while True:
            chunk = file.read(64 * 1024)
            if not chunk:
                break
            write(chunk)
        write(b'\r\n')
    for arg_name in params:
        value = params[arg_name]
        write(b'--%s\r\n' % (boundary_bytes,))
        write(b'Content-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (arg_name.encode(), value.encode()))
    write(b'--%s--\r\n' % (boundary_bytes,))

def async_post(async_client, url, files, params):
    boundary = uuid.uuid4().hex
    headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary}
    producer = partial(body_producer, boundary, files, params)
    response = async_client.fetch(url, method='POST', headers=headers, body_producer=producer)
    return response

def size_pretty(size):
    result = ''
    try:
        if size > 1024 * 1014 * 1024 * 1024:
            result = '%.3f T' % (size / 1024.0 / 1024.0 / 1024.0 / 1024.0)
        elif size > 1024 * 1014 * 1024:
            result = '%.3f G' % (size / 1024.0 / 1024.0 / 1024.0)
        elif size > 1024 * 1024:
            result = '%.3f M' % (size / 1024.0 / 1024.0)
        elif size > 1024:
            result = '%.3f K' % (size / 1024.0)
        else:
            result = '%d B' % size
    except Exception as e:
        LOG.exception(e)
        result = '0 B'
    return result

def disk_usage(dir_path=None):
    if not dir_path:
        dir_path = CONFIG['data_path']
    usage = psutil.disk_usage(dir_path)
    return {'total': usage.total, 'used': usage.used, 'free': usage.free, 'percent': usage.percent}