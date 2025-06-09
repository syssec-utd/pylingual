import pandas as pd
from airflow_commons.resources.glossary import COMMA, WHITE_SPACE
from airflow_commons.logger import get_logger
from airflow_commons.resources.bigquery import DEDUPLICATION_GET_AVAILABLE_PARTITIONS_FIELD_SQL_FILE, ARCHIVE_SOURCE_STATEMENT_FILE, ARCHIVE_DELETE_WHERE_STATEMENT_FILE
from airflow_commons.internal.bigquery.auth import connect
from airflow_commons.internal.bigquery.defaults import TIMEOUT, LOCATION, SELECT_RETURN_TYPE
from airflow_commons.internal.bigquery.core import get_time_partition_field, single_value_select, query, select, query_information_schema, get_table_ref, get_primitive_column_list, get_job_config
from airflow_commons.internal.bigquery.query import get_deduplication_source_statement, get_merge_sql, get_delete_sql, get_deduplication_additional_merge_conditions
from airflow_commons.internal.util.file_utils import read_sql
from airflow_commons.internal.util.time_utils import get_buffered_timestamp

class BigqueryOperator(object):

    def __init__(self, service_account_file: str):
        """
        Initializes a BigqueryOperator instance
        :param service_account_file: relative location of service account file
        :return:
        """
        self.ARCHIVE_MODES = ['INSERT', 'UPSERT']
        self.DEFAULT_PRIMARY_KEYS = ['id']
        self.ARCHIVE_DEFAULT_PRIMARY_KEYS = ['id', 'last_updated_at', 'processed_at']
        self.DEFAULT_TIME_COLUMNS = ['last_updated_at', 'processed_at']
        self.client = connect(service_account_file)
        self.logger = get_logger('BigqueryOperator')

    def deduplicate(self, start_date: str, end_date: str, project_id: str, source_dataset: str, source_table: str, target_dataset: str, target_table: str, oldest_allowable_target_partition: str, primary_keys=None, time_columns=None, allow_partition_pruning: bool=True, job_priority: str=None, timeout=TIMEOUT, location=LOCATION):
        """
        Runs a merge query to deduplicate rows in historic table, and write to target snapshot table

        :param start_date: deduplication interval start
        :param end_date: deduplication interval end
        :param project_id: Bigquery project id
        :param source_dataset: source dataset id
        :param source_table: source table id
        :param target_dataset: target dataset id
        :param target_table: target table id
        :param oldest_allowable_target_partition: oldest value of time partition column value to be added to target table, aims to keep partition count below limit
        :param primary_keys: primary key columns of the source and target tables
        :param time_columns: time columns list to order rows
        :param allow_partition_pruning: partition pruning allow parameter, if true prunes target table's partitions to limit query size
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :param timeout: query timeout duration parameter
        :param location: query location parameter
        :return:
        """
        job_config = get_job_config(job_priority)
        if primary_keys is None:
            primary_keys = self.DEFAULT_PRIMARY_KEYS
        if time_columns is None:
            time_columns = self.DEFAULT_TIME_COLUMNS
        buffered_start_date = get_buffered_timestamp(start_date)
        source_partition_field = get_time_partition_field(self.client, source_dataset, source_table)
        partition_pruning_params = dict()
        additional_merge_conditions = None
        partition_pruning_params['target_partition_field'] = get_time_partition_field(self.client, target_dataset, target_table)
        if allow_partition_pruning:
            partition_pruning_params['available_target_partitions'] = single_value_select(client=self.client, sql=read_sql(sql_file=DEDUPLICATION_GET_AVAILABLE_PARTITIONS_FIELD_SQL_FILE, project_id=project_id, source_dataset=source_dataset, source_table=source_table, target_partition_field=partition_pruning_params['target_partition_field'], source_partition_field=source_partition_field, start_date=buffered_start_date, end_date=end_date, oldest_allowable_target_partition=oldest_allowable_target_partition))
            if partition_pruning_params['available_target_partitions'] is None:
                self.logger.info(f'There is no data: - {project_id}.{source_dataset}.{source_table} - between [{start_date} - {end_date}] .')
                return None
            additional_merge_conditions = get_deduplication_additional_merge_conditions(partition_pruning_params=partition_pruning_params)
        source_statement = get_deduplication_source_statement(start_date=buffered_start_date, end_date=end_date, project_id=project_id, source_dataset=source_dataset, source_table=source_table, source_partition_field=source_partition_field, primary_keys=primary_keys, time_columns=time_columns, oldest_allowable_target_partition=oldest_allowable_target_partition, allow_partition_pruning=allow_partition_pruning, partition_pruning_params=partition_pruning_params)
        sql = get_merge_sql(client=self.client, project_id=project_id, target_dataset=target_dataset, target_table=target_table, source_statement=source_statement, primary_keys=primary_keys, mode='UPSERT', additional_merge_conditions=additional_merge_conditions)
        return query(client=self.client, job_config=job_config, sql=sql, timeout=timeout, location=location)

    def upsert(self, source_statement_file: str, project_id: str, target_dataset: str, target_table: str, source_statement_params: dict=None, primary_keys=None, additional_merge_conditions: str=None, job_priority: str=None, timeout=TIMEOUT, location=LOCATION):
        """
        Runs a merge query to upsert target table, with given source statement, merge conditions, and primary keys

        :param source_statement_file: relative location of source statement file
        :param project_id: Bigquery project id
        :param target_dataset: targeted dataset id
        :param target_table: targeted table id
        :param source_statement_params: parameters of source statement
        :param primary_keys: target table's primary key list
        :param additional_merge_conditions: additional user specified merge conditions as string
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :param timeout: query timeout duration in seconds
        :param location: query location parameter
        :return:
        """
        job_config = get_job_config(job_priority)
        if source_statement_params is None:
            source_statement_params = dict()
        if primary_keys is None:
            primary_keys = self.DEFAULT_PRIMARY_KEYS
        source_statement = read_sql(sql_file=source_statement_file, **source_statement_params)
        sql = get_merge_sql(client=self.client, project_id=project_id, target_dataset=target_dataset, target_table=target_table, source_statement=source_statement, primary_keys=primary_keys, mode='UPSERT', additional_merge_conditions=additional_merge_conditions)
        return query(client=self.client, job_config=job_config, sql=sql, timeout=timeout, location=location)

    def insert(self, source_statement_file: str, project_id: str, target_dataset: str, target_table: str, source_statement_params: dict=None, primary_keys=None, additional_merge_conditions: str=None, job_priority: str=None, timeout=TIMEOUT, location=LOCATION):
        """
        Runs a merge query to insert non-existing rows to target table, with given source statement, merge conditions, and primary keys

        :param source_statement_file: relative location of source statement file
        :param project_id: Bigquery project id
        :param target_dataset: targeted dataset id
        :param target_table: targeted table id
        :param source_statement_params: parameters of source statement
        :param additional_merge_conditions: additional user specified merge conditions as string
        :param primary_keys: target table's primary key list
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :param timeout: query timeout duration in seconds
        :param location: query location parameter
        :return:
        """
        job_config = get_job_config(job_priority)
        if source_statement_params is None:
            source_statement_params = dict()
        if primary_keys is None:
            primary_keys = self.DEFAULT_PRIMARY_KEYS
        source_statement = read_sql(sql_file=source_statement_file, **source_statement_params)
        sql = get_merge_sql(client=self.client, project_id=project_id, target_dataset=target_dataset, target_table=target_table, source_statement=source_statement, primary_keys=primary_keys, mode='INSERT', additional_merge_conditions=additional_merge_conditions)
        return query(client=self.client, job_config=job_config, sql=sql, timeout=timeout, location=location)

    def write_query_results_to_destination(self, sql_file: str, timeout: int, location: str, destination_dataset: str, destination_table: str, write_disposition: str, sql_params: dict=None, job_priority: str=None):
        """
        :param sql_file: relative location of sql file to read sql from
        :param timeout: job timeout parameter
        :param location: job location parameter
        :param destination_dataset: id of the destination dataset
        :param destination_table: id of the destination table
        :param write_disposition: write disposition of query results
        :param sql_params: sql parameters dictionary
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :return:
        """
        job_config = get_job_config(job_priority, write_disposition)
        job_config.allow_large_results = True
        job_config.destination = get_table_ref(self.client, destination_dataset, destination_table)
        if sql_params is None:
            sql_params = dict()
        sql = read_sql(sql_file=sql_file, **sql_params)
        return query(self.client, job_config, sql, timeout, location)

    def get_query_results(self, sql_file: str, return_type: str=SELECT_RETURN_TYPE, sql_params: dict=None, timeout: int=TIMEOUT, location: str=LOCATION, index_label: str=None, job_priority: str=None):
        """
        Runs query and returns the result as dataframe

        :param return_type: file format to be returned (dict,dataframe,csv,json,json_string,pyarrow); default is dataframe
        :param sql_file: relative location of sql file to read sql from
        :param sql_params: sql parameters dictionary
        :param timeout: query timeout duration in seconds
        :param location: query location parameter
        :param index_label: if given and return type is csv, table will be indexed with this column name
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :return: query result
        """
        if sql_params is None:
            sql_params = dict()
        sql = read_sql(sql_file=sql_file, **sql_params)
        return select(client=self.client, sql=sql, timeout=timeout, location=location, return_type=return_type, index_label=index_label, job_priority=job_priority)

    def get_single_value_query_results(self, sql_file: str, sql_params: dict=None, job_priority: str=None, timeout=TIMEOUT, location=LOCATION):
        """
        Runs a single value returning query and returns the result

        :param sql_file: relative location of sql file to read sql from
        :param sql_params: sql parameters dictionary
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :param timeout: query timeout duration in seconds
        :param location: query location parameter
        :return: query result
        """
        if sql_params is None:
            sql_params = dict()
        sql = read_sql(sql_file=sql_file, **sql_params)
        return single_value_select(client=self.client, sql=sql, job_priority=job_priority, timeout=timeout, location=location)

    def delete(self, project_id: str, dataset_id: str, table_id: str, where_statement_file: str, where_statement_params: dict=None, job_priority: str=None, timeout=TIMEOUT, location=LOCATION):
        """
        Runs a delete query on given table, and removes rows that conform where condition

        :param project_id: Bigquery project id
        :param dataset_id: dataset id
        :param table_id: table id
        :param where_statement_file: relative location of where statement sql file
        :param where_statement_params: parameters of where statements
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :param timeout: query timeout duration in seconds
        :param location: query location parameter
        :return: query result
        """
        job_config = get_job_config(job_priority)
        if where_statement_params is None:
            where_statement_params = dict()
        where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
        sql = get_delete_sql(project_id=project_id, dataset_id=dataset_id, table_id=table_id, where_statement=where_statement)
        return query(client=self.client, job_config=job_config, sql=sql, timeout=timeout, location=location)

    def archive(self, archive_date: str, project_id: str, source_dataset: str, source_table: str, target_dataset: str, target_table: str, primary_keys: list=None, mode: str='INSERT', job_priority: str=None, timeout=TIMEOUT, location=LOCATION):
        """
        Archives selected rows on target non-partitioned table.

        :param archive_date: archive date
        :param project_id: Bigquery project id
        :param source_dataset: source dataset id
        :param source_table: source table id
        :param target_dataset: target dataset id
        :param target_table: target table id
        :param primary_keys: primary key columns of the source and target tables
        :param mode: archive mode, INSERT only inserts non-existing rows and UPSERT updates and inserts
        :param job_priority: priority of bigquery job, it is currently BATCH or INTERACTIVE (default)
        :param timeout: query timeout duration in seconds
        :param location: query location parameter
        :return:
        """
        if mode not in self.ARCHIVE_MODES:
            raise ValueError('Invalid archive mode:{}. Acceptable column names are '.format(mode) + (COMMA + WHITE_SPACE).join((i for i in self.ARCHIVE_MODES)))
        if primary_keys is None or primary_keys == []:
            primary_keys = get_primitive_column_list(self.client, project_id, source_dataset, source_table)
        source_statement_params = dict()
        source_statement_params['project_id'] = project_id
        source_statement_params['source_dataset'] = source_dataset
        source_statement_params['source_table'] = source_table
        source_statement_params['archive_date'] = archive_date
        source_statement_params['source_partition_field'] = get_time_partition_field(client=self.client, dataset_id=source_dataset, table_id=source_table)
        if mode == 'INSERT':
            self.insert(source_statement_file=ARCHIVE_SOURCE_STATEMENT_FILE, project_id=project_id, target_dataset=target_dataset, target_table=target_table, source_statement_params=source_statement_params, primary_keys=primary_keys, job_priority=job_priority, timeout=timeout, location=location)
        elif mode == 'UPSERT':
            self.upsert(source_statement_file=ARCHIVE_SOURCE_STATEMENT_FILE, project_id=project_id, target_dataset=target_dataset, target_table=target_table, source_statement_params=source_statement_params, primary_keys=primary_keys, job_priority=job_priority, timeout=timeout, location=location)
        delete_where_statement_params = dict()
        delete_where_statement_params['archive_date'] = archive_date
        delete_where_statement_params['source_partition_field'] = source_statement_params['source_partition_field']
        self.delete(project_id=project_id, dataset_id=source_dataset, table_id=source_table, where_statement_file=ARCHIVE_DELETE_WHERE_STATEMENT_FILE, where_statement_params=delete_where_statement_params, job_priority=job_priority, timeout=timeout, location=location)

    def list_tables(self, project_id: str, dataset_id: str):
        """
        Returns a list of all tables in a dataset

        :param project_id: Bigquery project id
        :param dataset_id: dataset id
        :return: List
        """
        return query_information_schema(client=self.client, requested_column_name='table_name', project_id=project_id, dataset_id=dataset_id)

    def insert_to_table_from_dataframe(self, dataset_id: str, table_name: str, data: pd.DataFrame()):
        """
        Inserts dataframe to the specified table. Returns list of errors for each row

        :param dataset_id: Bigquery dataset id
        :param table_name: Table name to insert rows
        :param data: Data to be inserted into the table
        :return: Sequence[Sequence[Mappings]]: A list with insert errors for each insert chunk.
        :raises: ValueError: if table's schema is not set
        """
        table_ref = get_table_ref(client, dataset_id, table_name)
        table = self.client.get_table(table_ref)
        return self.client.insert_rows_from_dataframe(table, data)

    def load_to_table_from_dataframe(self, dataset_id: str, table_name: str, write_disposition: str, data: pd.DataFrame()):
        """
        Loads dataframe to the specified table. Returns list of errors for each row

        :param dataset_id: Bigquery dataset id
        :param table_name: Table name to insert rows
        :param write_disposition: write disposition of query results
        :param data: Data to be inserted into the table
        :return This instance:
        :raises: ValueError: If a usable parquet engine cannot be found. This method requires :mod:`pyarrow` to be installed
        """
        job_config = get_job_config(job_priority='', write_disposition=write_disposition, job_config_str='LoadJobConfig')
        table_ref = get_table_ref(self.client, dataset_id, table_name)
        return self.client.load_table_from_dataframe(data, table_ref, job_config=job_config).result()