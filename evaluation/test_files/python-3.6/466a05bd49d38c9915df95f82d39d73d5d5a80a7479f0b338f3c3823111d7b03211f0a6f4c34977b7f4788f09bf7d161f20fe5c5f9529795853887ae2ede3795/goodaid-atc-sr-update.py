import os
import sys
sys.path.append('../../../..')
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
from zeno_etl_libs.logger import get_logger
from dateutil.tz import gettz
import numpy as np
import pandas as pd
import datetime as dt
import argparse
parser = argparse.ArgumentParser(description='This is ETL script.')
parser.add_argument('-e', '--env', default='dev', type=str, required=False)
(args, unknown) = parser.parse_known_args()
env = args.env
os.environ['env'] = env
logger = get_logger()
logger.info(f'env: {env}')
table_name = 'goodaid-atc-sr'
rs_db = DB()
rs_db.open_connection()
s3 = S3()
gs = GoogleSheet()
data = gs.download(data={'spreadsheet_id': '1JMt8oICcodWbzHqQg3DckHKFrJAR0vXmFVXOunW-38Q', 'sheet_name': 'Sheet1', 'listedFields': []})
data = pd.DataFrame(data)
data['drug_id'] = data['drug_id'].astype(str).astype(int)
logger.info('Data: G-sheet data fetched successfully')
logger.info(len(data))
data.drop(['drug_name', 'composition'], axis=1, inplace=True)
drug_id_list = data.drug_id.unique()
drug_id_list = tuple(drug_id_list)
query = '\nselect id as "drug_id", "drug-name", composition from "prod2-generico".drugs d where id in {} '
data_name = rs_db.get_df(query.format(drug_id_list))
data = pd.merge(left=data, right=data_name, how='inner', on='drug_id')
query = '\n        select\n            d.id as "drug_id",\n            MIN(bi."created-at") as "start-date",\n            d."composition-master-id"\n        from\n            "prod2-generico"."bill-items-1" bi\n        left join "prod2-generico"."inventory-1" i on\n            bi."inventory-id" = i.id\n        left join "prod2-generico".drugs d on\n            i."drug-id" = d.id\n        where\n            d."company-id" = 6984\n            and d.id in {}\n            and bi."created-at" is not null\n        group by\n            d.id,\n            d."composition-master-id"  '
min_date = rs_db.get_df(query.format(drug_id_list))
logger.info('Data: min-composition start date fetched successfully')
logger.info(len(min_date))
merged = pd.merge(left=data, right=min_date, how='inner', on='drug_id')
merged['start-date'] = pd.to_datetime(merged['start-date']).dt.date
merged['start-date'] = pd.to_datetime(merged['start-date'])
logger.info(len(merged))
gaid_comp_min_date = f'\n        select\n            MIN(bi."created-at") as "min-bill-date",\n            d."composition-master-id"\n        from\n            "prod2-generico"."bill-items-1" bi\n        left join "prod2-generico"."inventory-1" i on\n            bi."inventory-id" = i.id\n        left join "prod2-generico".drugs d on\n            i."drug-id" = d.id\n        where\n            d."company-id" = 6984\n        group by\n            d."composition-master-id"\n\n'
min_date_comp = rs_db.get_df(gaid_comp_min_date)
min_date_comp['rank'] = min_date_comp['min-bill-date'].rank().astype(int)
min_date_comp['lot'] = (min_date_comp['rank'] / 25).apply(np.ceil).astype(int)
logger.info('Data: min-composition start date, lot and rank fetched successfully')
logger.info(len(min_date_comp))
goodaid_tagging = pd.merge(left=merged, right=min_date_comp, how='left', on='composition-master-id')
goodaid_tagging.columns = goodaid_tagging.columns.str.replace(' ', '-')
goodaid_tagging.columns = goodaid_tagging.columns.str.replace('_', '-')
goodaid_tagging['created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
goodaid_tagging['created-by'] = 'etl-automation'
goodaid_tagging['updated-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
goodaid_tagging['updated-by'] = 'etl-automation'
logger.info(len(goodaid_tagging))
schema = 'prod2-generico'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)
truncate_query = f' DELETE FROM "{schema}"."{table_name}" '
rs_db.execute(truncate_query)
logger.info(f'Table:{table_name} table truncated')
s3.write_df_to_db(df=goodaid_tagging[table_info['column_name']], table_name=table_name, db=rs_db, schema=schema)
logger.info(f'Table:{table_name} table uploaded')
rs_db.close_connection()