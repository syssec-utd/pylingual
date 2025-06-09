"""
@File    :   Docker.py
@Time    :   2022-10-25 20:57
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   Docker管理功能
"""
from plbm.Cmd import ComMand
from plbm.Jurisdiction import Jurisdiction
from plbm.Logger import ColorLogger
from plbm.Package import PackageManagement
from sys import exit
from plbm.FileManagement import FileManagement
from plbm.Service import ServiceManagement

class DockerManagement:

    def __init__(self, password, logs=True, log_file=None, journal=False):
        """
		Docker管理
		:param password: 主机密码
		:param logs: 是否开启日志
		:param log_file: 日志文件路径
		:param journal: 是否记录日志到文件
		"""
        self.logs = logs
        self.logger = ColorLogger(file=log_file, txt=journal, class_name=self.__class__.__name__)
        ju = Jurisdiction(passwd=password)
        if not ju.verification(name='DockerManagement'):
            self.logger.error('当前用户/密码无法获取sudo权限: %s' % password)
            exit(1)
        self.cmd = ComMand(password=password, logs=logs)
        self.pac = PackageManagement(password=password, logs=logs, file=log_file, package='docker.io')
        self.fm = FileManagement()
        self.service = ServiceManagement(service='docker.service', password=password, log=logs)

    def check_install(self):
        if not self.pac.installed():
            if not self.pac.installed(pac='docker-ce'):
                self.logger.error('未安装Docker.io/Docker-ce')
                return False
        return True

    def mirror(self, url='https://mirror.ccs.tencentyun.com'):
        """
		更改/新增镜像地址
		:param url: 镜像地址
		:return:
		"""
        txt = '{\n\t"registry-mirrors": ["%s"]\n}' % url
        try:
            with open(file='daemon.json', mode='w', encoding='utf-8') as w:
                w.write(txt)
                w.close()
        except Exception as e:
            self.logger.error(str(e))
            return False
        try:
            self.fm.copyfile(src='daemon.json', dst='/etc/docker/daemon.json', cover=True)
        except Exception as e:
            self.logger.error(str(e))
            return False
        try:
            self.service.restart(reload=True)
        except Exception as e:
            self.logger.error(str(e))
            return False
        return True