"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import datetime
import time
import pytz
from django.utils import timezone
DEFAULT_MULTIPLICATOR = 1
SHOW_TZ = False
FMT_LENGTH = None if SHOW_TZ else 16

def timeformat_to_timestamp(timeformat, time_multiplicator=DEFAULT_MULTIPLICATOR):
    """
    时间格式 -> 时间戳
    :param {str} timeformat: 日期格式字符串
    :param {int} time_multiplicator: 时间倍数
    :return: 时间戳
    """
    if not timeformat:
        return None
    if type(timeformat) in [str]:
        timestamp = int(time.mktime(time.strptime(timeformat, '%Y-%m-%d %H:%M:%S')))
    else:
        timestamp = int(timeformat.strftime('%s'))
    return int(timestamp * time_multiplicator)

def timestamp_to_datetime(from_timestamp, time_multiplicator=DEFAULT_MULTIPLICATOR):
    """
    时间戳 -> datetime
    :param {int} from_timestamp: 时间戳
    :param {int} time_multiplicator: 时间倍数
    :return: 时间戳
    """
    utc_tz = pytz.timezone('UTC')
    utc_dt = utc_tz.localize(datetime.datetime.utcfromtimestamp(int(from_timestamp) / time_multiplicator))
    return utc_dt

def format_datetime(o_datetime):
    """
    格式化日志对象展示格式

    :param {datetime} o_datetime datetime实例
    :return 格式化时间字符串
    """
    return o_datetime.strftime('%Y-%m-%d %H:%M:%S%z')

def strftime_local(aware_time, fmt='%Y-%m-%d %H:%M:%S'):
    """
    格式化aware_time为本地时间
    :param {datetime} aware_time 时间字段
    :param {string} fmt 时间format格式
    :return 格式化时间字符串
    """
    if not aware_time:
        return None
    if timezone.is_aware(aware_time):
        aware_time = timezone.localtime(aware_time)
    return aware_time.strftime(fmt)

def localtime_to_timezone(d_time, to_zone):
    """
    将时间字符串根据源时区转为用户时区
    :param {datetime} d_time 时间
    :param {string} to_zone 时区
    :return 用户时区时间
    """
    zone = pytz.timezone(to_zone)
    return d_time.astimezone(zone)

def time_to_string(date_time):
    """
    传入一个标准时间，返回其字符串形式
    :param {datetime} date_time: 时间
    :return: 时间字符串
    """
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

def date_to_string(_data):
    """
    传入一个标准日期，返回其字符串形式
    :param {datetime} _data: 日期
    :return: 日期字符串
    """
    return _data.strftime('%Y-%m-%d')

def string_to_time(t_str):
    """
    传入一个字符串，返回其标准时间格式
    :param {string} t_str: 时间字符串
    :return: 时间
    """
    return datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')

def string_to_date(d_str):
    """
    传入一个字符串，返回其标准日期格式
    :param {string} d_str: 日期字符串
    :return: 日期
    """
    return datetime.datetime.strptime(d_str, '%Y-%m-%d')