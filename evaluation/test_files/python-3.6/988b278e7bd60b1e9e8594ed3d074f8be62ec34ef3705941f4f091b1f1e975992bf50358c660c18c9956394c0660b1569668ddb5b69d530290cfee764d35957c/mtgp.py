import sys
import os
from mtlibs.docker_helper import isInContainer
from mtlibs import process_helper
from pathlib import Path
import logging
from dotenv import load_dotenv, find_dotenv
import json
import logging
import shlex
import subprocess
import time
from os.path import relpath
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import re
from os import path
import argparse
from mtlibs.github import gitclone, gitParseOwnerRepo
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
load_dotenv('.env')
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_env():
    env_names = ['GIT_TOKEN', 'DOCKER_HUB_USER', 'DOCKER_HUB_PASSWORD']
    for item in env_names:
        print(f'---{item}')
        if not os.environ.get(item):
            print(f'error: need env {item}')
            return False
    return True

def gitpod_clone_private_repo(giturl: str):
    """
        给定git 网址，下载到指定路径并根据规则运行相关代码。
    """
    logger.info(f'giturl {giturl}')
    parsed = urlparse(giturl)
    if not parsed.hostname:
        logger.error(f'url incorrect : {giturl}')
        return
    uri = parsed
    (owner, repo, file) = gitParseOwnerRepo(giturl)
    clone_to = path.join('/workspace', repo)
    gitclone(owner, repo, parsed.username, clone_to)
    if not file:
        logger.info('no entry script,skip launch')
    if file:
        file = file.lstrip('/')
        scriptFile = path.join(clone_to, file)
        if not Path(scriptFile).exists():
            logger.warn(f'入口文件不存在{scriptFile}')
        Path(scriptFile).chmod(448)
        logger.info(f'[TODO]开始执行入口文件 {scriptFile}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls')
    args = parser.parse_args()
    logger.info(f'urls: {args.urls}')
    logger.info(f'urls: {args.urls}')
    gitup_urls = args.urls or os.environ.get('MTX_GITUP')
    if not gitup_urls:
        logger.info(f'need urls')
        exit()
    items = gitup_urls.split('|')
    for item in items:
        gitpod_clone_private_repo(item)
if __name__ == '__main__':
    main()