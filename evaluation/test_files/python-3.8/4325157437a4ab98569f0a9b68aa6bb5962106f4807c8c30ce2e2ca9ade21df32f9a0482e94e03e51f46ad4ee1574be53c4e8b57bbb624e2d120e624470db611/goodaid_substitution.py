"""
Author - vishal.gupta@generico.in
Objective - rework the safety stock numbers based on good aid composition
Only for one top SKU and Good Aid SKU ss will be set
"""
import numpy as np
import pandas as pd

def get_ga_composition_sku(db, schema, substition_type=['generic'], logger=None):
    """ to get good aid sku and top sku """
    ga_sku_query = '\n            select wh."drug-id" , d.composition \n            from "{schema}"."wh-sku-subs-master" wh\n            left join "{schema}".drugs d \n            on d.id = wh."drug-id" \n            where wh."add-wh" = \'Yes\'\n            and d."company-id" = 6984\n            and d.type in {0}\n            '.format(str(substition_type).replace('[', '(').replace(']', ')'), schema=schema)
    ga_sku = db.get_df(ga_sku_query)
    ga_sku.columns = [c.replace('-', '_') for c in ga_sku.columns]
    logger.info('GoodAid SKU list ' + str(ga_sku.shape[0]))
    ga_active_composition = tuple(ga_sku['composition'].values)
    top_sku_query = '\n            select wh."drug-id" , d.composition \n            from "{schema}"."wh-sku-subs-master" wh\n            left join "{schema}".drugs d \n            on d.id = wh."drug-id" \n            where wh."add-wh" = \'Yes\'\n            and d."company-id" != 6984\n            and d.type in {0}\n            and d.composition in {1}\n            '.format(str(substition_type).replace('[', '(').replace(']', ')'), str(ga_active_composition), schema=schema)
    top_sku = db.get_df(top_sku_query)
    top_sku.columns = [c.replace('-', '_') for c in top_sku.columns]
    logger.info('GoodAid comp Top SKU list ' + str(top_sku.shape[0]))
    rest_sku_query = '\n            select id as drug_id, composition\n            from "{schema}".drugs\n            where composition in {0}\n            and id not in {1}\n            and type in {2}\n            '.format(str(ga_active_composition), str(tuple(top_sku['drug_id'].values)), str(substition_type).replace('[', '(').replace(']', ')'), schema=schema)
    rest_sku = db.get_df(rest_sku_query)
    logger.info('GoodAid comp rest SKU list ' + str(rest_sku.shape[0]))
    return (ga_sku, top_sku, rest_sku)

def update_ga_ss(safety_stock_df, store_id, db, schema, ga_inv_weight=0.5, rest_inv_weight=0, top_inv_weight=1, substition_type=['generic'], min_column='safety_stock', ss_column='reorder_point', max_column='order_upto_point', logger=None):
    """updating safety stock for good aid """
    good_aid_ss_log = pd.DataFrame()
    pre_max_qty = safety_stock_df[max_column].sum()
    logger.info('Getting SKU list')
    (ga_sku, top_sku, rest_sku) = get_ga_composition_sku(db, schema, substition_type, logger)
    logger.info('Aggregating composition level SS')
    ga_composition = pd.concat([ga_sku, top_sku, rest_sku], axis=0)
    columns_list = ['drug_id', 'composition', min_column, ss_column, max_column]
    ga_composition_ss = ga_composition.merge(safety_stock_df, on='drug_id')[columns_list]
    ga_composition_ss_agg = ga_composition_ss.groupby(['composition'])[min_column, ss_column, max_column].sum().reset_index()
    rest_sku_index = safety_stock_df[safety_stock_df['drug_id'].isin(rest_sku['drug_id'])].index
    top_sku_index = safety_stock_df[safety_stock_df['drug_id'].isin(top_sku['drug_id'])].index
    ga_sku_index = safety_stock_df[safety_stock_df['drug_id'].isin(ga_sku['drug_id'])].index
    logger.info('Updating safety stock')
    prev_rest_sku_ss = safety_stock_df.loc[rest_sku_index].merge(rest_sku)[columns_list]
    prev_rest_sku_ss['sku_type'] = 'rest generic'
    good_aid_ss_log = good_aid_ss_log.append(prev_rest_sku_ss)
    safety_stock_df.loc[rest_sku_index, min_column] = np.round(rest_inv_weight * safety_stock_df.loc[rest_sku_index, min_column])
    safety_stock_df.loc[rest_sku_index, ss_column] = np.round(rest_inv_weight * safety_stock_df.loc[rest_sku_index, ss_column])
    safety_stock_df.loc[rest_sku_index, max_column] = np.round(rest_inv_weight * safety_stock_df.loc[rest_sku_index, max_column])
    prev_top_sku_ss = safety_stock_df.loc[top_sku_index].merge(top_sku)[columns_list]
    prev_top_sku_ss['sku_type'] = 'top generic'
    good_aid_ss_log = good_aid_ss_log.append(prev_top_sku_ss)
    safety_stock_df.loc[top_sku_index, min_column] = np.round(top_inv_weight * safety_stock_df.loc[top_sku_index, min_column])
    safety_stock_df.loc[top_sku_index, ss_column] = np.round(top_inv_weight * safety_stock_df.loc[top_sku_index, ss_column])
    safety_stock_df.loc[top_sku_index, max_column] = np.round(top_inv_weight * safety_stock_df.loc[top_sku_index, max_column])
    prev_ga_sku_ss = safety_stock_df.loc[ga_sku_index].merge(ga_sku)[columns_list]
    prev_ga_sku_ss['sku_type'] = 'good aid'
    good_aid_ss_log = good_aid_ss_log.append(prev_ga_sku_ss)
    ga_sku_ss = ga_composition_ss_agg.merge(ga_sku)[columns_list]
    ga_sku_ss[min_column] = np.round(ga_inv_weight * ga_sku_ss[min_column])
    ga_sku_ss[ss_column] = np.round(ga_inv_weight * ga_sku_ss[ss_column])
    ga_sku_ss[max_column] = np.round(ga_inv_weight * ga_sku_ss[max_column])
    ss_df_columns = safety_stock_df.columns
    safety_stock_df = safety_stock_df.merge(ga_sku_ss, how='left', on=['drug_id'])
    safety_stock_df[min_column] = np.max(safety_stock_df[[min_column + '_y', min_column + '_x']], axis=1)
    safety_stock_df[ss_column] = np.max(safety_stock_df[[ss_column + '_y', ss_column + '_x']], axis=1)
    safety_stock_df[max_column] = np.max(safety_stock_df[[max_column + '_y', max_column + '_x']], axis=1)
    safety_stock_df = safety_stock_df[ss_df_columns]
    ga_sku_new_entries = ga_sku_ss.loc[~ga_sku_ss['drug_id'].isin(safety_stock_df['drug_id'])]
    if len(ga_sku_new_entries) > 0:
        ga_sku_new_entries_drug_list = str(list(ga_sku_new_entries['drug_id'])).replace('[', '(').replace(']', ')')
        ga_sku_drug_info_query = '\n            select d.id as drug_id, "drug-name" as drug_name, type,\n                coalesce(doi."drug-grade", \'NA\') as drug_grade\n            from "{schema}".drugs d left join "{schema}"."drug-order-info" doi\n            on d.id = doi."drug-id"\n            where d.id in {0}\n            and doi."store-id" = {1}\n            '.format(ga_sku_new_entries_drug_list, store_id, schema=schema)
        ga_sku_drug_info = db.get_df(ga_sku_drug_info_query)
        ga_sku_new_entries = ga_sku_new_entries.merge(ga_sku_drug_info)
        ga_sku_new_entries['model'] = 'NA'
        ga_sku_new_entries['bucket'] = 'NA'
        ga_sku_new_entries['fcst'] = 0
        ga_sku_new_entries['std'] = 0
        ga_sku_new_entries['lead_time_mean'] = 0
        ga_sku_new_entries['lead_time_std'] = 0
        ga_sku_new_entries['correction_flag'] = 'N'
        safety_stock_df = safety_stock_df.append(ga_sku_new_entries)[ss_df_columns]
    good_aid_ss_log.insert(loc=0, column='store_id', value=store_id)
    good_aid_ss_log.rename(columns={min_column: 'safety_stock', ss_column: 'reorder_point', max_column: 'order_upto_point'}, inplace=True)
    post_max_qty = safety_stock_df[max_column].sum()
    print('Reduction in max quantity:', str(round(100 * (1 - post_max_qty / pre_max_qty), 2)) + '%')
    return (safety_stock_df, good_aid_ss_log)