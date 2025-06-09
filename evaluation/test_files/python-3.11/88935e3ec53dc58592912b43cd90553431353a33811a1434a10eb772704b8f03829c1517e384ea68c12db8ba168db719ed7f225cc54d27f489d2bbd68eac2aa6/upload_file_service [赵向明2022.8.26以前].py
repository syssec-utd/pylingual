import base64
import hashlib
import os
import re
import time
from rest_framework import serializers
from config.config import Config
from xj_resource.utils.model_handle import parse_model
from ..models import ResourceFile
from ..utils.digit_algorithm import DigitAlgorithm

class UploadFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResourceFile
        fields = ['id', 'user_id', 'title', 'url', 'filename', 'format', 'md5', 'snapshot']

def robust(actual_do):

    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except Exception as e:
            print(str(e))
    return add_robust

class UploadFileService(object):
    base_path = Config.absolute_path
    to_month = time.strftime('%Y-%m', time.localtime(time.time()))
    folder_path = Config.getIns().get('xj_resource', 'FILE_UPLOAD_DIR', '/upload/file/') + to_month + '/'
    save_path = None
    filename = None
    input_file = None
    file_info = {}
    old_filename = None
    new_filename = None
    suffix = None
    __is_valid = True
    __error_message = None

    def __init__(self, input_file):
        self.input_file = input_file
        self.file_code = input_file.read()
        self.validate()

    def validate(self):
        if self.input_file is None:
            self.__set_error('请选择文件')
            return False
        ret = re.search('(.*)\\.(\\w{3,4})$', self.input_file.name)
        if not ret:
            self.__set_error('上传的文件名不合法')
            return False
        self.old_filename = ret.group(1)
        self.suffix = ret.group(2)
        file_format_list = Config.getIns().get('xj_resource', 'file_format_list')
        if file_format_list:
            file_format_list = file_format_list.split(',')
            if file_format_list:
                if not self.suffix in file_format_list:
                    self.__set_error('上传的文件类型不合法')
                    return False

    def get_md5(self):
        content_md5 = hashlib.md5()
        content_md5.update(self.file_code)
        content_base64 = base64.b64encode(content_md5.digest())
        return content_base64.decode('utf-8')

    def write_disk(self):
        try:
            if not self.__is_valid:
                return False
            path = self.base_path + '/' + self.folder_path
            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.exists(self.save_path):
                with open(self.save_path, 'wb') as f:
                    f.write(self.file_code)
        except Exception as e:
            self.__set_error(str(e))

    def write_oss(self, config):
        pass

    def save_to_db(self, save_data):
        try:
            if not self.__is_valid:
                return False
            md5 = save_data.get('md5', None)
            if md5 is None:
                return False
            instance = ResourceFile.objects.filter(md5=md5).first()
            if not instance:
                serializer = UploadFileSerializer(save_data)
                return serializer.save()
            return instance
        except Exception as e:
            self.__set_error(str(e))
            return False

    def info_detail(self):
        try:
            file_md5 = self.get_md5()
            instance = parse_model(ResourceFile.objects.filter(md5=file_md5))
            if instance:
                instance = instance[0]
                self.save_path = (self.base_path + instance['url']).replace('//', '/')
                return instance
            '获取文件信息并返回'
            self.new_filename = 'file_' + DigitAlgorithm.make_unicode_16() + '.' + self.suffix
            self.save_path = (self.base_path + self.folder_path + self.new_filename).replace('//', '/')
            self.file_info = {'url': Config.getIns().get('xj_resource', 'host') + (self.folder_path + self.new_filename).replace('//', '/'), 'filename': self.new_filename, 'format': self.suffix, 'md5': file_md5, 'snapshot': {'old_filename': self.old_filename, 'suffix': self.suffix}}
            return self.file_info
        except Exception as e:
            self.__set_error(str(e))
            return {}

    def __set_error(self, error_message):
        if not self.__error_message:
            self.__error_message = error_message
        self.__is_valid = False

    def is_valid(self):
        return self.__is_valid

    def get_error_message(self):
        return self.__error_message