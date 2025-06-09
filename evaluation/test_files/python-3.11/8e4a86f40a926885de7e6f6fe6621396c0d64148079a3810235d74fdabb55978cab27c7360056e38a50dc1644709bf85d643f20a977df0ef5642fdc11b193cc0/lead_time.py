import numpy as np
import datetime as dt
'\nSteps -\n1. Get Auto short total time -> from creation to received at store\n2. If marked as lost make it 7 days\n3. Max LT capped at 7 days\n'

def lead_time(store_id, cal_sales, reset_date, db, schema, logger=None):
    sb_creation_delay_ethical = 1
    sb_creation_delay_other = 1
    sb_creation_delay_generic = 2
    end_date = str((dt.datetime.strptime(reset_date, '%Y-%m-%d') - dt.timedelta(7)).date())
    begin_date = str(cal_sales.date.dt.date.max() - dt.timedelta(97))
    logger.info('Lead Time Calculation Starts')
    logger.info(f'SB Begin Date: {begin_date}, SB End Date: {end_date}')
    lead_time_query = f"""\n            select "store-id" , "drug-id" , "type" , status , "created-to-delivery-hour" as "lt-hrs"\n            from "{schema}"."as-ms" am \n            where "as-ms" = 'AS'\n            and "store-id" = {store_id}\n            and date("created-at") <= '{end_date}'\n            and date("created-at") >= '{begin_date}'\n            and status not in ('failed', 'deleted')\n            """
    lead_time = db.get_df(lead_time_query)
    lead_time.columns = [c.replace('-', '_') for c in lead_time.columns]
    lead_time['type'] = np.where(lead_time['type'].isin(['ethical', 'high-value-ethical']), 'ethical', lead_time['type'])
    lead_time['type'] = np.where(lead_time['type'].isin(['ethical', 'generic']), lead_time['type'], 'others')
    lead_time['lt_days'] = lead_time['lt_hrs'] / 24
    lead_time['lt_days'] = lead_time['lt_days'].fillna(7)
    lead_time['lt_days'] = np.where(lead_time['lt_days'] > 7, 7, lead_time['lt_days'])
    lead_time['lt_days'] = np.select([lead_time['type'] == 'generic', lead_time['type'] == 'ethical'], [lead_time['lt_days'] + sb_creation_delay_generic, lead_time['lt_days'] + sb_creation_delay_ethical], default=lead_time['lt_days'] + sb_creation_delay_other)
    lt_store_mean = round(lead_time.lt_days.mean(), 2)
    lt_store_std = round(lead_time.lt_days.std(ddof=0), 2)
    lt_drug = lead_time.groupby('drug_id').agg({'lt_days': [np.mean, np.std]}).reset_index()
    lt_drug.columns = ['drug_id', 'lead_time_mean', 'lead_time_std']
    lt_drug['lead_time_std'] = np.where(lt_drug['lead_time_std'].isin([0, np.nan]), lt_store_std, lt_drug['lead_time_std'])
    logger.info('Lead Time Calculation Completed')
    return (lt_drug, lt_store_mean, lt_store_std)