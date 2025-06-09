from lib.common import *
from lib.cache import *
from lib.countdown_latch import CountDownLatch
from bin.base_commond import Command
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import json
import os
import logging
import argparse
ExceptionData = {}

class InstallCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        self.baseDir = self.config.get('BASE_DIR')
        self.cfgPath = self.config.get('CFG_PATH')
        self.packetJsonPath = self.config.get('PACKET_JSON_PATH')
        self.regionRepository = self.config.get('REGION_REPOSITORY')

    def add_options(self) -> None:
        self.parser.add_argument('-c', type=str, help='cfg file path')
        self.parser.add_argument('-p', type=str, help='packet file path')
        self.parser.add_argument('-r', type=str, help='install dir, base dir')
        self.parser.add_argument('-i', type=str, help='regiion image')

    def dealWithAgs(self, *args) -> None:
        (args, argsElse) = self.parser.parse_known_args(args[1], args[0])
        if args.r:
            self.baseDir = args.r
        if args.c:
            self.cfgPath = args.c
        if args.p:
            self.packetJsonPath = args.p
        if args.i:
            self.regionRepository = args.i

    def run(self, *args) -> int:
        self.dealWithAgs(*args)
        createDir(self.baseDir)
        createDir(self.baseDir + self.config.get('TOOL_DIR'))
        pool = ThreadPoolExecutor(max_workers=os.cpu_count())
        cache = Cache(self.baseDir)
        toolInfos = readFileJson(self.packetJsonPath)
        latch = CountDownLatch(len(toolInfos['cmds']))
        for tool in toolInfos['cmds']:
            pool.submit(self.downloadTool, tool, cache, latch)
        latch.await_()
        if 'exception' in ExceptionData:
            logging.error('子线程发生异常:', ExceptionData['exception'])
            raise RuntimeError('子线程发生异常: ')
        modules = readCfg(self.cfgPath)
        latch = CountDownLatch(len(modules))
        for module in modules:
            pool.submit(self.downloadModule, module, cache, latch)
        latch.await_()
        if 'exception' in ExceptionData:
            logging.error('子线程发生异常:', ExceptionData['exception'])
            raise RuntimeError('子线程发生异常: ')

    def downloadModule(self, module: list, cache: Cache, latch: CountDownLatch) -> None:
        try:
            if module[0] != '&':
                return
            key = self.baseDir + self.config.get('DOWNLOAD_LIST_FILE_LOCK_PATH') + module[1] + '-' + module[2] + '.lock'
            with FileLock(key):
                if not cache.checkInLocalList(module[1] + '-' + module[2]):
                    module[3] = module[3].replace('./', '/')
                    createDir(self.baseDir + module[3] + '/' + module[2])
                    parsed_url = urlparse(self.regionRepository)
                    protocol = parsed_url.scheme
                    host = parsed_url.netloc
                    nexusResponse = httpGet(f'{protocol}://{host}' + '/service/rest/v1/search/assets', {'group': module[3] + '/' + module[2], 'repository': 'rd-repo-packet-qa'})
                    fileInfoJsonData = json.loads(nexusResponse.text)
                    if len(fileInfoJsonData['items']) == 1 and iscompress(fileInfoJsonData['items'][0]['path']):
                        downloadFileWithZip(fileInfoJsonData['items'][0]['downloadUrl'], self.config.get('BASE_DIR') + module[3] + '/' + module[2], os.path.basename(fileInfoJsonData['items'][0]['path']), True)
                    else:
                        for fileInfo in fileInfoJsonData['items']:
                            downloadFileByUrl(fileInfo['downloadUrl'], self.baseDir + module[3] + '/' + module[2] + '/' + os.path.basename(fileInfo['path']))
                    cache.addInLocalList(module[1] + '-' + module[2])
                    return
        except Exception as e:
            global ExceptionData
            ExceptionData['exception'] = e
            logging.error('下载失败:' + module['0'])
        finally:
            latch.count_down()

    def downloadTool(self, tool: list, cache: Cache, latch: CountDownLatch):
        try:
            key = self.baseDir + self.config.get('DOWNLOAD_LIST_FILE_LOCK_PATH') + tool['name'] + '-' + tool['version'] + '.lock'
            with FileLock(key):
                if not cache.checkInLocalList(tool['name'] + '-' + tool['version']):
                    downloadFileWithZip(self.regionRepository + '/' + self.config.get('TOOL_DIR') + '/' + tool['name'], self.baseDir + self.config.get('TOOL_DIR'), tool['name'], True)
                    cache.addInLocalList(tool['name'] + '-' + tool['version'])
                    return
        except Exception as e:
            global ExceptionData
            ExceptionData['exception'] = e
            logging.error('下载失败:' + tool['name'], e)
        finally:
            latch.count_down()