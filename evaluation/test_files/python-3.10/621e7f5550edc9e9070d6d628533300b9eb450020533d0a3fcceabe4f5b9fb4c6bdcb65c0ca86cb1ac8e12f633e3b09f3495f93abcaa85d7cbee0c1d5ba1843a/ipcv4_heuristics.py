from ast import literal_eval
import pandas as pd
import numpy as np

def ipcv4_heuristics(final_pred_ss_df, drug_type_list_v4, db, schema):
    """ drug_tupe_list_v4 variable has format as
        drug_type_list_v4 = {'generic':'{0:[0,0,0], 1:[0,0,1], 2:[0,1,2],3:[1,2,3]}',
        'ethical':'{0:[0,0,0], 1:[0,0,1], 2:[0,1,2],3:[1,2,3]}',
        'others':'{0:[0,0,0], 1:[0,0,2], 2:[0,1,2],3:[1,2,3]}'}

    final_pred_ss_df has the following format Index(['drug_id', 'model', 'bucket', 'percentile', 'fcst', 'std',
   'lead_time_mean', 'lead_time_std', 'safety_stock', 'reorder_point',
   'order_upto_point', 'safety_stock_days', 'reorder_days',
   'order_upto_days', 'fptr', 'curr_inventory', 'max_value',
   'correction_flag'],
   dtype='object')
    """
    q_drug_type_info = f' select id as drug_id, "type" as drug_type from "{schema}".drugs '
    drug_type_info = db.get_df(q_drug_type_info)
    drug_type_info['drug_type'] = np.where((drug_type_info['drug_type'] == 'ethical') | (drug_type_info['drug_type'] == 'generic'), drug_type_info['drug_type'], 'others')
    final_pred_ss_df_v4 = pd.merge(final_pred_ss_df, drug_type_info, on=['drug_id'], how='left')
    for drug_type in drug_type_list_v4.keys():
        for (max_value, ops_value) in literal_eval(drug_type_list_v4[drug_type]).items():
            safety_stock = ops_value[0]
            reorder_point = ops_value[1]
            order_upto_point = ops_value[2]
            index_list = final_pred_ss_df_v4[final_pred_ss_df_v4['order_upto_point'].isin([max_value]) & (final_pred_ss_df_v4['drug_type'] == drug_type)].index
            final_pred_ss_df_v4.loc[index_list, 'safety_stock'] = safety_stock
            final_pred_ss_df_v4.loc[index_list, 'reorder_point'] = reorder_point
            final_pred_ss_df_v4.loc[index_list, 'order_upto_point'] = order_upto_point
            print('Cases with {0} max: {1} for drug_type:{2} '.format(max_value, len(index_list), drug_type))
    final_pred_ss_df_v4 = final_pred_ss_df_v4.drop(['drug_type'], axis=1)
    return final_pred_ss_df_v4