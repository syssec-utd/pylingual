from rolling_king.autotest.db.sqlalchemy_util import AlchemyUtil
from rolling_king.autotest.db.db_models import CaseRecordDecoder, CaseRecordModel, ExecutionRecordDecoder
import logging
import configparser
import json
import os
import time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('requests.http_sender_module')

class BaseTest(object):
    conf_absolute_path = '../../../conf/'
    case_record_dict_list = []
    unique_tag = None
    execution_record_dict_list = []

    @staticmethod
    def _get_project_param_dict(project_conf_file_path):
        project_conf_file = open(project_conf_file_path)
        cf = configparser.ConfigParser()
        cf.read_file(project_conf_file)
        logger.info('从 %s 读取到 %d 个配置项。' % (project_conf_file_path, len(cf.items())))
        dict_val = {'test_project_name': cf.get('project', 'TEST_PROJECT_NAME'), 'test_psm': cf.get('project', 'TEST_PSM')}
        logger.info('项目参数 = %s' % dict_val)
        return dict_val

    @staticmethod
    def get_project_conf_dict():
        curr_sys_path = os.getcwd()
        index_of_com = curr_sys_path.find('com')
        if index_of_com != -1:
            BaseTest.conf_absolute_path = curr_sys_path[0:index_of_com] + 'com/conf/'
            project_param_dict = BaseTest._get_project_param_dict(BaseTest.conf_absolute_path + 'project.conf')
        else:
            project_param_dict = BaseTest._get_project_param_dict(curr_sys_path + '/com/conf/project.conf')
        return project_param_dict

    @staticmethod
    def analyze_func_desc(entire_desc):
        tested_inter_dict_val = {'test_interface': '', 'test_inter_type': '', 'test_description': ''}
        desc_list = entire_desc.split('\n')
        for seg in desc_list:
            if seg.find('desc') != -1:
                start_index_desc = seg.find('desc') + 5
                test_description = seg[start_index_desc:].strip()
                tested_inter_dict_val['test_description'] = test_description
            if seg.find('api_info') != -1:
                start_index_api_info = seg.find('api_info') + 9
                desc_dict_str = seg[start_index_api_info:].strip()
                api_dict = json.loads(desc_dict_str)
                protocol = api_dict['protocol_type']
                tested_inter_dict_val['test_inter_type'] = protocol
                if protocol == 'HTTP':
                    tested_inter_dict_val['test_interface'] = api_dict['inter_name'] + '::' + api_dict['inter_path']
                elif protocol == 'THRIFT':
                    tested_inter_dict_val['test_interface'] = api_dict['inter_name'] + '.' + api_dict['method_name']
                else:
                    logger.error('传入的protocol既不是HTTP也不是THRIFT。')
        logger.info('被测接口 = %s' % tested_inter_dict_val)
        return tested_inter_dict_val

    @staticmethod
    def _get_db_rela_conf_path(db_conf_path=None):
        if db_conf_path is not None:
            return db_conf_path
        else:
            curr_sys_path = os.getcwd()
            logger.info(f'curr_sys_path={curr_sys_path}')
            index_of_com = curr_sys_path.find('com')
            if index_of_com != -1:
                BaseTest.conf_absolute_path = curr_sys_path[0:index_of_com] + 'com/conf/'
            else:
                logger.warning('被测路径不包含com。')
                BaseTest.conf_absolute_path = curr_sys_path + '/com/conf/'
            return BaseTest.conf_absolute_path + 'db.conf'

    @staticmethod
    def insert_update_delete():
        dict_val = AlchemyUtil.get_db_param_dict('DB_BOE_Site_Reldb', BaseTest._get_db_rela_conf_path())
        site_rel_db_engine = AlchemyUtil.init_engine(dict_val)
        site_rel_db_session = AlchemyUtil.get_session(site_rel_db_engine)
        case_change_flag = False
        project_conf_dict = BaseTest.get_project_conf_dict()
        criteria_set = {CaseRecordModel.test_psm == project_conf_dict['test_psm'], CaseRecordModel.test_project_name == project_conf_dict['test_project_name']}
        db_case_record_model_list = AlchemyUtil.query_obj_list(site_rel_db_session, CaseRecordModel, criteria_set=criteria_set)
        test_case_record_model_list = []
        for curr_case_dict in BaseTest.case_record_dict_list:
            test_case_record_model_list.append(CaseRecordDecoder.dict_to_obj(curr_case_dict))
        logger.info('DB中现有记录：%d 个。' % len(db_case_record_model_list))
        logger.info('本次测试记录：%s 个。' % len(test_case_record_model_list))
        if len(db_case_record_model_list) == 0:
            AlchemyUtil.insert_list_with_flush_only(site_rel_db_session, test_case_record_model_list)
            AlchemyUtil.do_commit_only(site_rel_db_session)
        elif len(test_case_record_model_list) > 0:
            curr_version_in_db = db_case_record_model_list[0].version
            matched_db_record_uid_list = []
            disuse_db_record_uid_list = []
            for db_case_model in db_case_record_model_list:
                logger.info('***当前 db_case_model: test_class=%s, test_method=%s, uid=%d' % (db_case_model.test_class, db_case_model.test_method, db_case_model.uid))
                for test_case_model in test_case_record_model_list:
                    logger.info('---当前 test_case_model: test_class=%s, test_method=%s' % (test_case_model.test_class, test_case_model.test_method))
                    if db_case_model.test_class == test_case_model.test_class and db_case_model.test_method == test_case_model.test_method:
                        logger.info('找到 test_class=%s, test_method=%s 的 uid=%d DB记录：%s' % (db_case_model.test_class, db_case_model.test_method, db_case_model.uid, db_case_model.to_json()))
                        test_case_model.uid = db_case_model.uid
                        logger.info('当前 test_case_model: test_class=%s, test_method=%s 设为 uid=%d' % (test_case_model.test_class, test_case_model.test_method, test_case_model.uid))
                        matched_db_record_uid_list.append(db_case_model.uid)
                        logger.info('当前 db_case_model uid=%d 加入匹配列表中' % db_case_model.uid)
                        break
                    else:
                        pass
                if db_case_model.uid not in matched_db_record_uid_list:
                    case_change_flag = True
                    disuse_db_record_uid_list.append(db_case_model.uid)
                    logger.info('DB中的 uid = %d 的记录作废，并加入作废列表中。' % db_case_model.uid)
                    del_row = AlchemyUtil.delete_for_criteria_commit(site_rel_db_session, CaseRecordModel, {CaseRecordModel.uid == db_case_model.uid})
                    logger.info('DB中的 uid = %d 的 %d 条记录从DB数据库中删除：' % (db_case_model.uid, del_row))
                else:
                    pass
            logger.info('匹配列表中的uid如下:')
            for matched_uid in matched_db_record_uid_list:
                logger.info('matched_uid = %d' % matched_uid)
            logger.info('作废列表中的uid如下:')
            for disuse_uid in disuse_db_record_uid_list:
                logger.info('disuse_uid = %d' % disuse_uid)
            logger.info('本次测试一共作废 %d 个DB中的用例记录。' % len(disuse_db_record_uid_list))
            new_case_count = 0
            for test_case_model in test_case_record_model_list:
                if test_case_model.uid == 0:
                    case_change_flag = True
                    AlchemyUtil.insert_obj_with_commit(site_rel_db_session, test_case_model)
                    new_case_count += 1
                else:
                    pass
            logger.info('本次测试一共新增 %d 个测试用例。' % new_case_count)
            if case_change_flag:
                logger.info('本次测试用例有变化。')
                new_version = curr_version_in_db + 1
                logger.info('new_version = %d' % new_version)
                update_dict = {'version': new_version, 'gmt_modify': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}
                affected_row = AlchemyUtil.update_for_criteria_with_commit(site_rel_db_session, CaseRecordModel, criteria_set, update_dict)
                logger.info('【Success】Totally, {0} Records have been updated with version = {1}.'.format(affected_row, new_version))
            else:
                logger.info('本次测试毫无变化，无用例新增、无用例删除。')
        else:
            logger.info('本次测试不包含任何测试用例。')

    @staticmethod
    def insert_execution_record():
        dict_val = AlchemyUtil.get_db_param_dict('DB_BOE_Site_Reldb', BaseTest.conf_absolute_path + 'db.conf')
        site_rel_db_engine = AlchemyUtil.init_engine(dict_val)
        site_rel_db_session = AlchemyUtil.get_session(site_rel_db_engine)
        for curr_execution_dict in BaseTest.execution_record_dict_list:
            logger.info('curr_execution_dict = %s' % curr_execution_dict)
            curr_execution_model = ExecutionRecordDecoder.dict_to_obj(curr_execution_dict)
            AlchemyUtil.insert_obj_without_commit(session=site_rel_db_session, obj=curr_execution_model)
        AlchemyUtil.do_commit_only(site_rel_db_session)
        logger.info('本次新增 %d 条测试执行记录并插入至DB。' % len(BaseTest.execution_record_dict_list))
if __name__ == '__main__':
    base_test = BaseTest()