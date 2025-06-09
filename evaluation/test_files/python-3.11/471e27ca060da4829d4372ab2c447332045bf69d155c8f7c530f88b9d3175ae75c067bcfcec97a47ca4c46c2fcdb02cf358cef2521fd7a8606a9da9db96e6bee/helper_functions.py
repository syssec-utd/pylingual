"""
Author  -   shubham.jangir@zeno.health
Objective   -   This module contains helper functions for new store ipc
"""
import numpy as np
Q_REPEATABLE = '\n    SELECT\n        id AS "drug-id",\n        "is-repeatable"\n    FROM\n        "{schema}".drugs\n    WHERE\n        "is-repeatable" = 1\n'
Q_PTR = '\n    select\n        "drug-id",\n        AVG(ptr) as ptr\n    FROM\n        "{schema}"."inventory-1"\n    GROUP BY\n        "drug-id"\n'
Q_STORES = '\n    select\n        id as "store-id",\n        name as "store-name"\n    FROM\n        "{schema}".stores\n'
Q_DRUG_INFO = '\n    select\n        id as "drug-id",\n        "drug-name",\n        type,\n        category\n    FROM\n        "{schema}".drugs\n'

def prep_data_from_sql(query_pass, db):
    data_fetched = db.get_df(query_pass)
    data_fetched.columns = [c.replace('-', '_') for c in data_fetched.columns]
    return data_fetched

def query_drug_grade(store_id, schema):
    query = '\n        SELECT\n            "drug-id",\n            "drug-grade"\n        FROM\n            "{schema}"."drug-order-info"\n        WHERE\n            "store-id" = {0}\n        '.format(store_id, schema=schema)
    return query

def query_max_zero(store_id, schema):
    query = '\n    SELECT\n        "store-id",\n        "drug-id"\n    FROM\n        "{schema}"."drug-order-info"\n    WHERE\n        "store-id" = {0}\n        and max = 0\n    '.format(store_id, schema=schema)
    return query

def query_inventory(store_id, schema):
    query = '\n    SELECT\n        "store-id",\n        "drug-id",\n        SUM(quantity) AS "current-inventory"\n    FROM\n        "{schema}"."inventory-1"\n    WHERE\n        "store-id" = {0}\n    GROUP BY\n        "store-id",\n        "drug-id"\n    '.format(store_id, schema=schema)
    return query

def get_drug_info(store_id, db, schema):
    q_inv = query_inventory(store_id, schema)
    data_inv = prep_data_from_sql(q_inv, db)
    data_ptr = prep_data_from_sql(Q_PTR.format(schema=schema), db)
    data_ptr['ptr'] = data_ptr['ptr'].astype(float)
    data_drug_info = prep_data_from_sql(Q_DRUG_INFO.format(schema=schema), db)
    q_drug_grade = query_drug_grade(store_id, schema)
    data_drug_grade = prep_data_from_sql(q_drug_grade, db)
    data_stores = prep_data_from_sql(Q_STORES.format(schema=schema), db)
    return (data_inv, data_ptr, data_drug_info, data_drug_grade, data_stores)

def order_value_report(ss_drug_sales):
    ss_drug_sales['to_order_quantity'] = np.where(ss_drug_sales['current_inventory'] < ss_drug_sales['safety_stock'], ss_drug_sales['max'] - ss_drug_sales['current_inventory'], 0)
    ss_drug_sales['to_order_value'] = ss_drug_sales['to_order_quantity'] * ss_drug_sales['ptr']
    order_value = ss_drug_sales.groupby(['type', 'store_name', 'drug_grade']).agg({'to_order_quantity': 'sum', 'to_order_value': 'sum'}).reset_index()
    return order_value