"""
Insert USGS acquisitions into reporting DB
"""
import os
import json
from nemo_reporting.dea.common import reporting_db_usgs
from nemo_reporting.utilities import logging, s3
log = logging.set_logger('automated_reporting.usgs_inserts')

def gen_m2m_api_inserts(rep_conn, m2mApiMatrix):
    """
    Insert M2M API metadata into DB
    :param m2mApiMatrix:
    :return:
    """
    conn, cursor = reporting_db_usgs.open_cursor(rep_conn)
    for row in m2mApiMatrix:
        executionStr = 'INSERT INTO landsat.usgs_l1_nrt_c2_stac_listing (scene_id, wrs_path, wrs_row,\n        collection_category, collection_number, sat_acq) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;'
        params = (row[0], row[1], row[2], row[3], int(row[4]), row[5])
        reporting_db_usgs.execute_query(executionStr, params, cursor)
    return reporting_db_usgs.conn_commit(conn, cursor)

def convert_m2m_to_matrix(acquisitions):
    """
    Modifies the results to of M2M API call
    to a list of lists(matrix) for use in this task.
    """
    matrix_output = []
    for item in acquisitions:
        matrix_output.append([item['id'], item['wrs2'].split('_')[0], item['wrs2'].split('_')[1], item['collect_cat'], item['collect_num'], item['acq_time']])
    return matrix_output

def task(rep_conn, s3_object_name, s3_creds):
    """
    Main function
    """
    acquisitions = s3.get_json(s3_creds, s3_object_name)
    log.info('Read acquistions from S3: {}'.format(len(acquisitions)))
    m2mApiMatrix = convert_m2m_to_matrix(acquisitions)
    log.debug(m2mApiMatrix)
    log.info('Inserting USGS inventory into DB: {} acquisitions'.format(len(m2mApiMatrix)))
    gen_m2m_api_inserts(rep_conn, m2mApiMatrix)

def task_env():
    """Call task using environment variables"""
    usgs_acq_xcom = str(os.getenv('USGS_ACQ_XCOM')).replace("'", '"')
    params = dict(s3_object_name=json.loads(usgs_acq_xcom)['s3_object'], rep_conn=dict(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT')), s3_creds=dict(bucket=os.getenv('S3_BUCKET'), access_key=os.getenv('S3_ACCESS_KEY'), secret_key=os.getenv('S3_SECRET_KEY')))
    task(**params)