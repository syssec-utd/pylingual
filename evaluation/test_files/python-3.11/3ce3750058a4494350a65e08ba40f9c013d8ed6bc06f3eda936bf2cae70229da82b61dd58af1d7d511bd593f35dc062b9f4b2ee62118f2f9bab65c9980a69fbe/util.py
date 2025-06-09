import datetime
import difflib
import logging
import os
import shutil
import subprocess
import tarfile
import pkg_resources
import requests
from servicefoundry.io.output_callback import OutputCallBack
from servicefoundry.lib.const import ENTITY_JSON_DATETIME_FORMAT
from servicefoundry.lib.exceptions import BadRequestException
logger = logging.getLogger()

def read_text(file_name, name=__name__):
    return pkg_resources.resource_string(name, file_name).decode('utf-8')

def read_lines_from_file(file_path):
    with open(file_path) as file:
        return [line.rstrip() for line in file.readlines()]

def read_text_from_file(file_path):
    with open(file_path) as file:
        return file.read()

def clean_dir(dir_name):
    if os.path.isfile(dir_name):
        os.remove(dir_name)
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 292) >> 2
    os.chmod(path, mode)

def create_file_from_content(file_name, content, executable=False):
    with open(file_name, 'w') as text_file:
        text_file.write(content)
    if executable:
        make_executable(file_name)

def upload_package_to_s3(metadata, package_file):
    with open(package_file, 'rb') as file_to_upload:
        http_response = requests.put(metadata['url'], data=file_to_upload)
        if http_response.status_code not in [204, 201, 200]:
            raise RuntimeError(f'Failed to upload to S3 {http_response.content}')

def request_handling(res):
    try:
        status_code = res.status_code
    except Exception:
        raise Exception("Unknown error occurred. Couldn't get status code.")
    if 200 <= status_code <= 299:
        if res.content == b'':
            return None
        return res.json()
    if 400 <= status_code <= 499:
        try:
            message = res.json()['message']
        except Exception:
            message = res
        raise BadRequestException(res.status_code, message)
    if 500 <= status_code <= 599:
        raise Exception(res.content)

def run_process(cmd, cwd=None):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, cwd=cwd)

def execute(cmd, cwd=None):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1, cwd=cwd)
    for stdout_line in iter(popen.stdout.readline, ''):
        yield stdout_line
    popen.stdout.close()
    for stderr_line in iter(popen.stderr.readline, ''):
        yield stderr_line
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, ' '.join(cmd))

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, 'w:gz') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def download_file(url, file_path):
    r = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(r.content)

def uncompress_tarfile(file_path, destination):
    file = tarfile.open(file_path)
    file.extractall(destination)
    file.close()

def get_file_diff(from_lines, to_lines, from_file='Original', to_file='Current'):
    return [line for line in difflib.unified_diff(from_lines, to_lines, fromfile=from_file, tofile=to_file, lineterm='')]

def manage_file_diff(source_lines, target_lines, entity, callback: OutputCallBack):
    diffs = get_file_diff(source_lines, target_lines, f'Original {entity}', f'Updated {entity}')
    if len(diffs) == 0:
        callback.print_line(f'No new changes are required in {entity}.')
    else:
        callback.print_line(f'Going to apply below changes in {entity}')
        callback.print_lines_in_panel(diffs, f'{entity} Diff')

def json_default_encoder(o):
    if isinstance(o, datetime.datetime):
        return o.strftime(ENTITY_JSON_DATETIME_FORMAT)