"""
@Author: HuangJianYi
@Date: 2022-04-24 15:15:19
@LastEditTime: 2023-04-19 15:37:09
@LastEditors: HuangJianYi
@Description: 
"""
import ast
import random
import decimal
import hashlib
from copy import deepcopy
from unittest import result
from asq.initiators import query
from urllib.parse import parse_qs, urlparse
from seven_framework.redis import *
from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_cloudapp_frame.handlers.filter_base import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.cryptography_helper import *
from seven_cloudapp_frame.libs.customize.riskmanage_helper import *
from seven_cloudapp_frame.models.enum import PlatType
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.operate_base_model import *
from seven_cloudapp_frame.models.user_base_model import *
from seven_cloudapp_frame.models.db_models.app.app_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.db_models.operation.operation_log_model import *

class FrameBaseHandler(BaseApiHandler):
    """
    :description: 公共handler基类
    """

    def get_http_log_extra_dict(self):
        """
        :Description: 获取http日志参数字典
        :last_editors: HuangJianYi
        """
        dict_param = {}
        if share_config.get_value('plat_type', 1) != PlatType.web.value:
            dict_param['open_id'] = self.get_open_id()
            if not dict_param['open_id']:
                dict_param['open_id'] = self.get_user_id()
        else:
            dict_param['open_id'] = self.get_cooke_user_id()
        dict_param['nick_name'] = self.get_user_nick()
        dict_param['app_id'] = self.get_app_id()
        dict_param['source_type'] = self._request_source_type()
        return dict_param

    def prepare(self):
        """
        :Description: 置于任何请求方法前被调用(请勿重写此函数,可重写prepare_ext)
        :last_editors: HuangJianYi
        """
        try:
            if self.__class__.__name__ == 'IndexHandler':
                return
            self.is_encrypt = False
            self._convert_request_params()
            dict_param = self.get_http_log_extra_dict()
            self._build_http_log(dict_param)
            if share_config.get_value('log_plain', True) == True and self.is_api_encrypt() == True:
                self.logging_link_info(f'plain_request_params:{self.json_dumps(self.request_params)}')
        except Exception as ex:
            if not hasattr(self, 'request_code'):
                self.request_code = UUIDHelper.get_uuid()
            self.logging_link_error('【公共handler基类】' + traceback.format_exc())

    def options_async(self):
        self.response_json_success()

    def check_xsrf_cookie(self):
        return

    def set_default_headers(self):
        allow_origin_list = share_config.get_value('allow_origin_list')
        if allow_origin_list:
            origin = self.request.headers.get('Origin')
            if origin in allow_origin_list:
                self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Headers', 'Origin,X-Requested-With,Content-Type,Accept,User-Token,Manage-ProductID,Manage-PageID,PYCKET_ID')
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,OPTIONS,PUT,DELETE')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def json_dumps(self, rep_dic):
        """
        :description: 将字典转化为字符串
        :param rep_dic：字典对象
        :return: str
        :last_editors: HuangJianYi
        """
        return SevenHelper.json_dumps(rep_dic)

    def json_loads(self, rep_str):
        """
        :description: 将字符串转化为字典
        :param rep_str：str
        :return: dict
        :last_editors: HuangJianYi
        """
        return SevenHelper.json_loads(rep_str)

    def get_param(self, param_name, default='', strip=True, filter_sql=False, filter_special_key=False):
        """
        :description: 二次封装获取参数
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param filter_sql: 是否过滤sql关键字
        :param filter_special_key: 是否过滤sql特殊字符
        :return: 参数值
        :last_editors: HuangJianYi
        """
        param_ret = ''
        if self.request_params:
            param_ret = self.request_params[param_name] if self.request_params.__contains__(param_name) else ''
        else:
            param_ret = self.get_argument(param_name, default, strip=strip)
        if param_ret == '' or param_ret == 'undefined':
            param_ret = default
        param_ret = RiskManageHelper.filter_routine_key(param_ret)
        if filter_sql == True:
            param_ret = RiskManageHelper.filter_sql(param_ret)
        if filter_special_key == True:
            param_ret = RiskManageHelper.filter_special_key(param_ret)
        return param_ret

    def get_param_int(self, param_name, default=0, strip=True, filter_sql=False, filter_special_key=False, throw_response_error=True, contain_list=[], range_list=[]):
        """
        :description: 二次封装获取参数转整形
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param filter_sql: 是否过滤sql关键字
        :param filter_special_key: 是否过滤sql特殊字符
        :param throw_response_error: 是否直接输出错误响应
        :param contain_list: 包含列表，举例：[1,2,3,4]
        :param range_list: 区间列表，只能有两个元素，举例：[1,10]
        :param filter_special_key: 是否过滤sql特殊字符
        :return: 转换后的参数值
        :last_editors: HuangJianYi
        """
        from tornado.web import Finish
        if not hasattr(self, 'param_error_list'):
            self.param_error_list = []
        param = self.get_param(param_name, default, strip, filter_sql, filter_special_key)
        (param, status) = SevenHelper.to_int(param, default, True)
        if status == False:
            log_info = {'param': param_name, 'type': 'int', 'info': '参数格式错误'}
            if throw_response_error == True:
                self.response_json_error('param_error', log_info['info'], log_info)
                raise Finish()
            else:
                self.param_error_list.append(log_info)
        else:
            if len(contain_list) > 0 and (not param in contain_list):
                log_info = {'param': param_name, 'type': 'int', 'info': '参数不在包含范围内'}
                if throw_response_error == True:
                    self.response_json_error('param_error', log_info['info'], log_info)
                    raise Finish()
                else:
                    self.param_error_list.append(log_info)
            if len(range_list) == 2 and (param < range_list[0] or param > range_list[1]):
                log_info = {'param': param_name, 'type': 'int', 'info': '参数不在区间范围内'}
                if throw_response_error == True:
                    self.response_json_error('param_error', log_info['info'], log_info)
                    raise Finish()
                else:
                    self.param_error_list.append(log_info)
        return param

    def get_param_decimal(self, param_name, default=0, strip=True, filter_sql=False, filter_special_key=False, throw_response_error=True):
        """
        :description: 二次封装获取参数转浮点
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param filter_sql: 是否过滤sql关键字
        :param filter_special_key: 是否过滤sql特殊字符
        :param throw_response_error: 是否直接输出错误响应
        :return: 转换后的参数值
        :last_editors: HuangJianYi
        """
        from tornado.web import Finish
        if not hasattr(self, 'param_error_list'):
            self.param_error_list = []
        param = self.get_param(param_name, default, strip, filter_sql, filter_special_key)
        (param, status) = SevenHelper.to_decimal(param, default, True)
        if status == False:
            log_info = {'param': param_name, 'type': 'decimal', 'info': '参数格式错误'}
            if throw_response_error == True:
                self.response_json_error('param_error', log_info['info'], log_info)
                raise Finish()
            else:
                self.param_error_list.append(log_info)
        return param

    def get_param_datetime(self, param_name, default='1900-01-01 00:00:00', strip=True, filter_sql=False, filter_special_key=False, throw_response_error=True, fmt='%Y-%m-%d %H:%M:%S'):
        """
        :description: 二次封装获取参数转时间
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param filter_sql: 是否过滤sql关键字
        :param filter_special_key: 是否过滤sql特殊字符
        :param throw_response_error: 是否直接输出错误响应
        :param fmt:时间格式化
        :return: 转换后的参数值
        :last_editors: HuangJianYi
        """
        from tornado.web import Finish
        if not hasattr(self, 'param_error_list'):
            self.param_error_list = []
        param = self.get_param(param_name, default, strip, filter_sql, filter_special_key)
        (param, status) = SevenHelper.to_date_time(param, fmt, default, True)
        if status == False:
            log_info = {'param': param_name, 'type': 'datetime', 'info': '参数格式错误'}
            if throw_response_error == True:
                self.response_json_error('param_error', log_info['info'], log_info)
                raise Finish()
            else:
                self.param_error_list.append(log_info)
        return param

    def is_api_encrypt(self):
        """
        :Description: 校验是否加密
        :last_editors: HuangJianYi
        """
        client_encrypt_type = share_config.get_value('client_encrypt_type', 0)
        server_encrypt_type = share_config.get_value('server_encrypt_type', 0)
        is_encrypt = False if hasattr(self, 'is_encrypt') and self.is_encrypt == False else True
        request_source_type = self._request_source_type()
        if is_encrypt == True and (request_source_type == 2 and server_encrypt_type == 1) or (request_source_type == 1 and client_encrypt_type == 1):
            return True
        else:
            return False

    def _request_source_type(self):
        """
        :Description: 请求来源类型 0-未知 1-client(客户端) 2-server(服务端)
        :last_editors: HuangJianYi
        """
        uri = self.request.uri
        if '/client/' in uri:
            return 1
        elif '/server/' in uri:
            return 2
        else:
            return share_config.get_value('source_type', 0)

    def _get_encrypt_appkey(self, json_params):
        """
        :Description: 获取加解密appkey,取值顺序：app_id ——> source_app_id ——> app_key ——> app_id
        :param json_params: json参数字典
        :last_editors: HuangJianYi
        """
        app_key = None
        if json_params:
            app_key = json_params.get('app_id', '')
            app_key = app_key if app_key else json_params.get('source_app_id', '')
        if not app_key:
            app_key = self.get_argument('app_id', '', strip=True)
            app_key = app_key if app_key else self.get_argument('source_app_id', '', strip=True)
            app_key = app_key if app_key else share_config.get_value('app_key')
            app_key = app_key if app_key else share_config.get_value('app_id')
        return app_key

    def _convert_request_params(self):
        """
        :Description: 转换请求参数 post请求：Content-type必须为application/json，前端必须对对象进行序列化转成json字符串，不能直接传对象,否则无法接收参数,存在特殊字符的参数必须进行url编码，否则+会被变成空值
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        self.request_params = {}
        self.content_type = ''
        if self.is_api_encrypt() == True:
            encrypt_key = share_config.get_value('encrypt_key', 'r8C1JpyAXxrFV26V')
            if hasattr(self, 'encrypt_key'):
                encrypt_key = self.encrypt_key
            json_params = None
            if 'Content-Type' in self.request.headers and self.request.headers['Content-type'].lower().find('application/json') >= 0 and self.request.body:
                self.content_type = 'application/json'
                json_params = json.loads(self.request.body)
            app_id = self._get_encrypt_appkey(json_params)
            if not app_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = 'param_error'
                invoke_result_data.error_message = '缺少必传参数'
                return invoke_result_data
            password = str(encrypt_key).replace('1', 'l')
            if self.content_type == 'application/json':
                try:
                    if json_params:
                        for field in json_params:
                            self.request_params[field] = json_params[field]
                        par = json_params['par'] if json_params.__contains__('par') else ''
                        if self.request.headers and self.request.headers['Referer'].lower().find('/devtools/') >= 0:
                            par = CodingHelper.url_decode(par)
                        dv = json_params['dv'] if json_params.__contains__('dv') else ''
                        if not par or not dv:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = 'error'
                            invoke_result_data.error_message = '参数解析错误'
                            return invoke_result_data
                        iv = app_id[0:10] + str(dv)[0:6] if len(str(dv)) >= 6 else ''
                        body_params = json.loads(CryptographyHelper.aes_decrypt(str(par), password, iv))
                        for field in body_params:
                            self.request_params[field] = body_params[field]
                except:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = 'error'
                    invoke_result_data.error_message = '参数解析错误'
                    return invoke_result_data
            else:
                for field in self.request.arguments:
                    self.request_params[field] = self.get_argument(field, '', strip=True)
                if 'par' in self.request.arguments and 'dv' in self.request.arguments:
                    par = self.get_argument('par', '', strip=True)
                    if self.request.headers and self.request.headers['Referer'].lower().find('/devtools/') >= 0:
                        par = CodingHelper.url_decode(par)
                    dv = self.get_argument('dv', '', strip=True)
                    iv = app_id[0:10] + str(dv)[0:6] if len(str(dv)) >= 6 else ''
                    try:
                        body_params = json.loads(CryptographyHelper.aes_decrypt(par, password, iv))
                        for field in body_params:
                            self.request_params[field] = body_params[field]
                    except:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = 'error'
                        invoke_result_data.error_message = '参数解析错误'
                        return invoke_result_data
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = 'error'
                    invoke_result_data.error_message = '参数解析错误'
                    return invoke_result_data
        elif 'Content-Type' in self.request.headers and self.request.headers['Content-type'].lower().find('application/json') >= 0 and self.request.body:
            try:
                self.content_type = 'application/json'
                json_params = json.loads(self.request.body)
                if json_params:
                    for field in json_params:
                        self.request_params[field] = json_params[field]
            except:
                pass
        else:
            for field in self.request.arguments:
                self.request_params[field] = self.get_argument(field, '', strip=True)
        return invoke_result_data

    def response_custom(self, rep_dic):
        """
        :description: 输出公共json模型
        :param rep_dic: 字典类型数据
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJianYi
        """
        self.http_response(self.json_dumps(rep_dic))

    def response_common(self, success=True, data=None, error_code='', error_message='', is_close_encrypt=False):
        """
        :description: 输出公共json模型
        :param success: 布尔值，表示本次调用是否成功
        :param data: 类型不限，调用成功（success为true）时，服务端返回的数据
        :param errorCode: 字符串，调用失败（success为false）时，服务端返回的错误码
        :param errorMessage: 字符串，调用失败（success为false）时，服务端返回的错误信息
        :param is_close_encrypt: 是否关闭输出加密（True-是 False-否）
        :return: 将dumps后的数据字符串返回给客户端   
        :last_editors: HuangJianYi
        """
        if hasattr(data, '__dict__'):
            data = data.__dict__
        template_value = {}
        template_value['success'] = success
        is_encrypt = False if hasattr(self, 'is_encrypt') and self.is_encrypt == False else True
        if is_encrypt == False:
            template_value['data'] = data
        elif self.is_api_encrypt() == True:
            json_params = None
            if hasattr(self, 'content_type') and self.content_type == 'application/json':
                json_params = json.loads(self.request.body)
            app_id = self._get_encrypt_appkey(json_params)
            if app_id and is_close_encrypt == False:
                dv = SevenHelper.get_random(16)
                encrypt_key = share_config.get_value('encrypt_key', 'r8C1JpyAXxrFV26V')
                if hasattr(self, 'encrypt_key'):
                    encrypt_key = self.encrypt_key
                password = str(encrypt_key).replace('1', 'l')
                iv = app_id[0:10] + str(dv)[0:6] if len(str(dv)) >= 6 else ''
                template_value['data'] = CryptographyHelper.aes_encrypt(self.json_dumps(data), password, iv)
                template_value['dv'] = dv
                if share_config.get_value('log_plain', True) == True:
                    self.logging_link_info(f'plain_response_data:{self.json_dumps(data)}')
            else:
                template_value['data'] = data
        else:
            template_value['data'] = data
        template_value['error_code'] = 'error' if not error_code and success == False else error_code
        template_value['error_message'] = '系统异常' if not error_message and success == False else error_message
        rep_dic = {}
        rep_dic['success'] = True
        rep_dic['data'] = template_value
        log_extra_dict = {}
        log_extra_dict['is_success'] = 1
        if success == False:
            log_extra_dict['is_success'] = 0
        self.http_reponse(self.json_dumps(rep_dic), log_extra_dict)

    def response_json_success(self, data=None, is_close_encrypt=False):
        """
        :description: 通用成功返回json结构
        :param data: 返回结果对象，即为数组，字典
        :param is_close_encrypt: 是否关闭输出加密（True-是 False-否）
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJianYi
        """
        self.response_common(data=data, is_close_encrypt=is_close_encrypt)

    def response_json_error(self, error_code='', error_message='', data=None, log_type=0):
        """
        :description: 通用错误返回json结构
        :param errorCode: 字符串，调用失败（success为false）时，服务端返回的错误码
        :param errorMessage: 字符串，调用失败（success为false）时，服务端返回的错误信息
        :param data: 返回结果对象，即为数组，字典
        :param log_type: 日志记录类型（0-不记录，1-info，2-error）
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJianYi
        """
        if log_type == 1:
            self.logging_link_info(f'{error_code}\n{error_message}\n{data}\n{self.request}')
        elif log_type == 2:
            self.logging_link_error(f'{error_code}\n{error_message}\n{data}\n{self.request}')
        self.response_common(False, data, error_code, error_message)

    def response_json_error_params(self):
        """
        :description: 通用参数错误返回json结构
        :param desc: 返错误描述
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJianYi
        """
        self.response_common(False, None, 'params error', '参数错误')

    def return_dict_error(self, error_code='', error_message=''):
        """
        :description: 返回error信息字典模型
        :param errorCode: 字符串，服务端返回的错误码
        :param errorMessage: 字符串，服务端返回的错误信息
        :return: dict
        :last_editors: HuangJianYi
        """
        rep_dic = {}
        rep_dic['error_code'] = error_code
        rep_dic['error_message'] = error_message
        self.logging_link_error(f'{error_code}\n{error_message}\n{self.request}')
        return rep_dic

    def get_now_datetime(self):
        """
        :description: 获取当前时间
        :return: str
        :last_editors: HuangJianYi
        """
        return SevenHelper.get_now_datetime()

    def create_order_id(self, ran=5):
        """
        :description: 生成订单号
        :param ran：随机数位数，默认5位随机数（0-5）
        :return: 25位的订单号
        :last_editors: HuangJianYi
        """
        return SevenHelper.create_order_id(ran)

    def get_app_key_secret(self):
        """
        :description: 获取app_key和app_secret
        :param 
        :return app_key, app_secret
        :last_editors: HuangJianYi
        """
        app_key = share_config.get_value('app_key')
        app_secret = share_config.get_value('app_secret')
        return (app_key, app_secret)

    def get_user_nick(self):
        """
        :description: 获取用户昵称
        淘宝小程序 如果要在test和online环境指定账号打开后台测试，需由前端写死传入
        :return str
        :last_editors: HuangJianYi
        """
        user_nick = self.get_param('nick_name')
        if not user_nick:
            user_nick = self.get_param('user_nick')
        plat_type = share_config.get_value('plat_type', 1)
        if plat_type == PlatType.tb.value:
            if self.get_param('source_app_id') == '':
                test_config = share_config.get_value('test_config', {})
                user_nick = test_config.get('user_nick', '')
        return user_nick

    def get_open_id(self):
        """
        :description: 获取open_id
        :return str
        :last_editors: HuangJianYi
        """
        open_id = self.get_param('open_id')
        plat_type = share_config.get_value('plat_type', 1)
        if plat_type == PlatType.tb.value:
            if self.get_param('source_app_id') == '':
                test_config = share_config.get_value('test_config', {})
                open_id = test_config.get('open_id', '')
        return open_id

    def get_user_id(self):
        """
        :description: 获取user_id,后续新项目统一使用user_code,tb_user_id和user_id只做兼容旧项目使用保留
        :param self
        :return str
        :last_editors: HuangJianYi
        """
        user_id = self.get_param_int('user_code')
        if user_id == 0:
            user_id = self.get_param_int('tb_user_id')
            if user_id == 0:
                user_id = self.get_param_int('user_id')
        return user_id

    def get_cooke_user_id(self):
        """
        :description: 获取cookie中的用户信息,适用场景H5
        :return:
        :last_editors: HuangJianYi
        """
        test_config = share_config.get_value('test_config', {})
        user_id = test_config.get('user_id', 0)
        if user_id <= 0:
            cookie_user_id = int(self.get_cookie('user_id', 0))
            cookie_user_id_md5 = self.get_cookie('user_id_md5', '')
            check_user_id_md5 = CryptoHelper.md5_encrypt(str(cookie_user_id), share_config.get_value('cookie_encrypt_key', 'r8C1JpyAXxrFV26V'))
            if cookie_user_id <= 0 or cookie_user_id_md5 != check_user_id_md5:
                user_id = 0
            else:
                user_id = cookie_user_id
        return user_id

    def set_cooke_user_id(self, user_id, expires_days=30):
        """
        :description: 设置user_id cookie
        :param user_id: 用户标识
        :param expires_days: 过期时间，单位天
        :return:
        :last_editors: HuangJianYi
        """
        user_id_md5 = CryptoHelper.md5_encrypt(str(user_id), share_config.get_value('cookie_encrypt_key', 'r8C1JpyAXxrFV26V'))
        self.set_cookie('user_id', str(user_id), expires_days=expires_days)
        self.set_cookie('user_id_md5', user_id_md5, expires_days=expires_days)
        self.set_cookie('user_token', UUIDHelper.get_uuid(), expires_days=expires_days)

    def get_source_app_id(self):
        """
        :description: 废弃使用,获取source_app_id(客户端client使用)，旧项目有用到要换成get_app_id
        :return str
        :last_editors: HuangJianYi
        """
        source_app_id = self.get_param('app_id')
        if source_app_id:
            return source_app_id
        source_app_id = self.get_param('source_app_id')
        plat_type = share_config.get_value('plat_type', 1)
        if plat_type == PlatType.tb.value:
            if source_app_id == share_config.get_value('client_template_id') or source_app_id == '':
                test_config = share_config.get_value('test_config', {})
                source_app_id = test_config.get('source_app_id', '')
        if not source_app_id:
            source_app_id = share_config.get_value('app_id')
        return source_app_id

    def get_app_id(self):
        """
        :description: 获取app_id
        :return str
        :last_editors: HuangJianYi
        """
        app_id = self.get_param('app_id')
        if app_id:
            return app_id
        plat_type = share_config.get_value('plat_type', 1)
        if plat_type == PlatType.tb.value:
            if self._request_source_type() == 2:
                user_nick = self.get_user_nick()
                if user_nick:
                    store_user_nick = user_nick.split(':')[0]
                    if store_user_nick:
                        app_info_model = AppInfoModel(context=self)
                        app_info_dict = app_info_model.get_cache_dict(where='store_user_nick=%s', limit='0,1', field='app_id', params=store_user_nick)
                        if app_info_dict:
                            app_id = app_info_dict['app_id']
            elif self._request_source_type() == 1:
                app_id = self.get_param('source_app_id')
                if app_id == share_config.get_value('client_template_id') or app_id == '':
                    test_config = share_config.get_value('test_config', {})
                    app_id = test_config.get('source_app_id', '')
        if not app_id:
            app_id = share_config.get_value('app_id')
        return app_id

    def get_access_token(self):
        """
        :description: 获取access_token
        :return str
        :last_editors: HuangJianYi
        """
        access_token = self.get_param('access_token')
        plat_type = share_config.get_value('plat_type', 1)
        if plat_type == PlatType.tb.value:
            env = self.get_param('env') if self.get_param('env') else config.get_value('env', '')
            test_config = share_config.get_value('test_config', {})
            if self.get_param('source_app_id') == '':
                access_token = test_config.get('access_token', '')
            elif env and env != 'online':
                user_nick = self.get_param('user_nick', '')
                store_user_nick = user_nick.split(':')[0]
                if store_user_nick and store_user_nick == test_config.get('user_nick', ''):
                    access_token = test_config.get('access_token', '')
        return access_token

    def get_act_id(self):
        """
        :description: 获取act_id 如果是测试环境，则默认取最新的活动，用于前端测试使用;如果都没有取配置文件的值，配置文件没配置设置默认值1;
        :return int
        :last_editors: HuangJianYi
        """
        act_id = self.get_param_int('act_id', -1)
        if act_id >= 0:
            return act_id
        app_id = self.get_app_id()
        env = self.get_param('env') if self.get_param('env') else config.get_value('env', '')
        if env and env != 'online' and app_id:
            act_info_model = ActInfoModel(context=self)
            condition_where = ConditionWhere()
            condition_where.add_condition('app_id=%s and is_release=1')
            params = [app_id]
            act_type = self.get_param_int('act_type', 0)
            if act_type > 0:
                condition_where.add_condition('act_type=%s')
                params.append(act_type)
            act_info_dict = act_info_model.get_cache_dict(where=condition_where.to_string(), order_by='id desc', field='id', params=params)
            if act_info_dict:
                act_id = act_info_dict['id']
                return act_id
        act_id = share_config.get_value('act_id', 1)
        return act_id

    def create_operation_log(self, operation_type=1, model_name='', handler_name='', old_detail=None, update_detail=None, operate_user_id='', operate_user_name='', operate_role_id='', title='', operation_desc=''):
        """
        :description: 创建操作日志
        :param operation_type：操作类型（查看枚举类OperationType）
        :param model_name：模块或表名称（跟配置表对应）
        :param handler_name：handler名称
        :param old_detail：变更前对象
        :param update_detail：变更后对象
        :param operate_user_id：操作人标识
        :param operate_user_name：操作人名称
        :param operate_role_id：操作人角色标识
        :param title：标题(对象)
        :param operation_desc：描述
        :param operation_ways：操作方式(1单一操作2批量操作)
        :return: 
        :last_editors: HuangJianYi
        """
        plat_type = share_config.get_value('plat_type', 1)
        if plat_type == PlatType.tb.value:
            if not operate_user_id:
                operate_user_id = self.get_open_id()
            if not operate_user_name:
                operate_user_name = self.get_user_nick()
        if not handler_name:
            handler_name = self.__class__.__name__
        operate_base_model = OperateBaseModel(context=self)
        operate_base_model.add_operation_log(operation_type, title, operation_desc, model_name, handler_name, old_detail, update_detail, self.get_app_id(), self.get_act_id(), operate_user_id, operate_user_name, operate_role_id, {'request_params': self.request_params, 'request': self.request}, self.get_remote_ip(), self.request_code)

    def check_continue_request(self, handler_name, app_id, object_id, expire=100):
        """
        :description: 一个用户同一handler频繁请求校验，只对同用户同接口同请求参数进行限制
        :param handler_name: handler名称
        :param app_id: 应用标识
        :param object_id: object_id(user_id或open_id)
        :param expire: 间隔时间，单位毫秒
        :return:满足频繁请求条件直接输出拦截
        :last_editors: HuangJianYi
        """
        result = (False, '')
        if object_id and handler_name and app_id:
            sign = CryptographyHelper.signature_md5(self.request_params)
            if SevenHelper.is_continue_request(f'continue_request:{handler_name}_{app_id}_{object_id}_{sign}', expire) == True:
                result = (True, f'操作太频繁,请{expire}毫秒后再试')
        return result

    def business_process_executing(self):
        """
        :description: 执行前事件
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = {}
        return invoke_result_data

    def business_process_executed(self, result_data, ref_params):
        """
        :description: 执行后事件
        :param result_data: result_data
        :param ref_params: 关联参数
        :return:
        :last_editors: HuangJianYi
        """
        return result_data

class ClientBaseHandler(FrameBaseHandler):
    """
    :description: 客户端handler基类
    """

    def prepare(self):
        """
        :Description: 置于任何请求方法前被调用(请勿重写此函数,可重写prepare_ext)
        :last_editors: HuangJianYi
        """
        if self.__class__.__name__ == 'IndexHandler':
            return
        try:
            invoke_result_data = self._convert_request_params()
            if invoke_result_data.success == False:
                self.request_code = UUIDHelper.get_uuid()
                self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
                self.finish()
                return
            dict_param = self.get_http_log_extra_dict()
            self._build_http_log(dict_param)
            is_api_encrypt = self.is_api_encrypt()
            if share_config.get_value('log_plain', True) == True and is_api_encrypt == True:
                self.logging_link_info(f'plain_request_params:{self.json_dumps(self.request_params)}')
            if is_api_encrypt == True:
                now_time = TimeHelper.get_now_timestamp(True)
                if self.request_params.__contains__('timestamp') and now_time - int(self.request_params['timestamp']) > int(1000 * 10):
                    self.response_json_error('timestamp', '超时操作')
                    self.finish()
                    return
            invoke_result_data = RiskManageHelper.check_attack_request()
            if invoke_result_data.success == False:
                self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
                self.finish()
                return
            if dict_param['open_id'] and self._request_source_type() == 1:
                (is_continue_request, error_message) = self.check_continue_request(self.__class__.__name__, dict_param['app_id'], dict_param['open_id'])
                if is_continue_request:
                    self.response_json_error('error', error_message)
                    self.finish()
                    return
                RiskManageHelper.add_current_limit_count(str(dict_param['app_id']), str(dict_param['open_id']))
            self.device_info_dict = self.get_device_info_dict()
        except Exception as ex:
            if not hasattr(self, 'request_code'):
                self.request_code = UUIDHelper.get_uuid()
            self.logging_link_error('【客户端handler基类】' + traceback.format_exc())

    def get_device_info_dict(self):
        """
        :description: 获取头部参数字典
        :last_editors: HuangJianYi
        """
        device_info_dict = {}
        clientheaderinfo_string = self.request.headers._dict.get('Clientheaderinfo')
        if clientheaderinfo_string:
            info_model = parse_qs(clientheaderinfo_string)
            device_info_dict['pid'] = info_model['pid'][0]
            device_info_dict['chid'] = 0 if 'chid' not in info_model.keys() else int(info_model['chid'][0])
            device_info_dict['height'] = 0 if 'height' not in info_model.keys() else int(float(info_model['height'][0]))
            device_info_dict['width'] = 0 if 'width' not in info_model.keys() else int(float(info_model['width'][0]))
            device_info_dict['version'] = '' if 'version' not in info_model.keys() else info_model['version'][0]
            device_info_dict['app_version'] = '' if 'app_version' not in info_model.keys() else info_model['app_version'][0]
            device_info_dict['net'] = '' if 'net' not in info_model.keys() else info_model['net'][0]
            device_info_dict['model_p'] = '' if 'model' not in info_model.keys() else info_model['model'][0]
            device_info_dict['lang'] = '' if 'lang' not in info_model.keys() else info_model['lang'][0]
            device_info_dict['ver_no'] = '' if 'ver_no' not in info_model.keys() else info_model['ver_no'][0]
            device_info_dict['timestamp'] = 0 if 'timestamp' not in info_model.keys() else int(info_model['timestamp'][0])
            device_info_dict['signature_md5'] = '' if 'signature_md5' not in info_model.keys() else info_model['signature_md5'][0]
        return device_info_dict

    def emoji_base64_to_emoji(self, text_str):
        """
        :description: 把加密后的表情还原
        :param text_str: 加密后的字符串
        :return: 解密后的表情字符串
        :last_editors: HuangJianYi 
        """
        return CryptographyHelper.emoji_base64_to_emoji(text_str)

    def emoji_to_emoji_base64(self, text_str):
        """
        :description: emoji表情转为[em_xxx]形式存于数据库,打包每一个emoji
        :description: 性能遇到问题时重新设计转换程序
        :param text_str: 未加密的字符串
        :return: 解密后的表情字符串
        :last_editors: HuangJianYi 
        """
        return CryptographyHelper.emoji_to_emoji_base64(text_str)