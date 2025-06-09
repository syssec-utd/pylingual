"""
@Author: HuangJianYi
@Date: 2021-07-26 09:40:36
@LastEditTime: 2021-09-10 16:11:30
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class StatOrmModel(CacheModel):

    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None):
        super(StatOrmModel, self).__init__(StatOrm, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

class StatOrm:

    def __init__(self):
        super(StatOrm, self).__init__()
        self.id = 0
        self.app_id = ''
        self.act_id = 0
        self.module_id = 0
        self.object_id = ''
        self.group_name = ''
        self.group_sub_name = ''
        self.key_name = ''
        self.key_value = ''
        self.value_type = 0
        self.repeat_type = 0
        self.sort_index = 0
        self.create_date = '1900-01-01 00:00:00'
        self.is_show = 0
        self.i1 = 0
        self.i2 = 0
        self.s1 = ''
        self.s2 = ''

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'module_id', 'object_id', 'group_name', 'group_sub_name', 'key_name', 'key_value', 'value_type', 'repeat_type', 'sort_index', 'create_date', 'is_show', 'i1', 'i2', 's1', 's2']

    @classmethod
    def get_primary_key(self):
        return 'id'

    def __str__(self):
        return 'stat_orm_tb'