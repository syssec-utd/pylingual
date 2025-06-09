"""
Element position api.
"""
import flybirds.core.global_resource as gr
from flybirds.core.plugin.plugins.default.ui_driver.poco import poco_position
import flybirds.utils.dsl_helper as dsl_helper

def position_not_change(context, param1, param2):
    poco_instance = gr.get_value('pocoInstance')
    param1_dict = dsl_helper.params_to_dic(param1)
    selector_str = param1_dict['selector']
    optional = {}
    if 'path' in param1_dict.keys():
        optional['path'] = param1_dict['path']
    elif 'multiSelector' in param1_dict.keys():
        optional['multiSelector'] = param1_dict['multiSelector']
    if 'timeout' in param1_dict.keys():
        optional['timeout'] = float(param1_dict['timeout'])
    else:
        optional['timeout'] = gr.get_frame_config_value('wait_ele_timeout', 10)
    param2_dict = dsl_helper.params_to_dic(param2, 'durTime')
    dur_time = float(param2_dict['durTime'])
    verify_count = gr.get_frame_config_value('verify_pos_not_change_count', 5)
    if 'verifyCount' in param2_dict.keys():
        verify_count = int(param2_dict['verifyCount'])
    poco_position.position_not_change(poco_instance, selector_str, optional, dur_time, verify_count)