from pyspark.sql.functions import udf, lit
from labelbox.schema.data_row_metadata import DataRowMetadataKind
from pyspark.sql.types import StructType, StructField, StringType, MapType, ArrayType
import json

def refresh_metadata_ontology(client):
    """ Refreshes a Labelbox Metadata Ontology
    Args:
        client              :   Required (labelbox.client.Client) - Labelbox Client object
    Returns 
        lb_mdo              :   labelbox.schema.data_row_metadata.DataRowMetadataOntology
        lb_metadata_names   :   List of metadata field names from a Labelbox metadata ontology
    """
    lb_mdo = client.lb_client.get_data_row_metadata_ontology()
    lb_metadata_names = [field['name'] for field in lb_mdo._get_ontology()]
    return (lb_mdo, lb_metadata_names)

def get_unique_values(spark_table, column_name):
    """ Grabs all unique values from a spark table column as strings
    Args:
        spark_table         :   Required (pyspark.sql.dataframe.Dataframe) - Databricks Spark Table object
        column_name         :   Required (str) - Spark Table column name
    Returns:
        List of unique values from a spark table column as strings
    """
    values = [str(x.__getitem__(column_name)) for x in spark_table.select(column_name).distinct().collect()]
    return values

def sync_metadata_fields(lb_client, spark_table, metadata_index={}):
    """ Ensures Labelbox's Metadata Ontology and Databricks Spark Table have all necessary metadata fields / columns given a metadata_index
    Args:
        client              :   Required (labelbox.client.Client) - Labelbox Client object
        spark_table         :   Required (pyspark.sql.dataframe.Dataframe) - Databricks Spark Table object
        metadata_index      :   Optional (dict) - Dictionary where {key=column_name : value=metadata_type} - metadata_type must be one of "enum", "string", "datetime" or "number"
    Returns:
        Updated spark_table, if columns were added from the metadata_index
    """
    (lb_mdo, lb_metadata_names) = refresh_metadata_ontology(lb_client)
    conversion = {'enum': DataRowMetadataKind.enum, 'string': DataRowMetadataKind.string, 'datetime': DataRowMetadataKind.datetime, 'number': DataRowMetadataKind.number}
    if metadata_index and spark_table:
        column_names = [str(col[0]) for col in spark_table.dtypes]
        for metadata_field_name in metadata_index.keys():
            if metadata_field_name not in column_names:
                spark_table = spark_table.withColumn(metadata_field_name, lit(None).cast(StringType()))
    metadata_index['lb_integration_source'] = 'string'
    for metadata_field_name in metadata_index.keys():
        metadata_type = metadata_index[metadata_field_name]
        if metadata_type not in conversion.keys():
            print(f'Error: Invalid value for metadata_index field {metadata_field_name} : {metadata_type}')
            return False
        if metadata_field_name not in lb_metadata_names:
            enum_options = get_unique_values(spark_table, metadata_field_name) if metadata_type == 'enum' else []
            lb_mdo.create_schema(name=metadata_field_name, kind=conversion[metadata_type], options=enum_options)
            (lb_mdo, lb_metadata_names) = refresh_metadata_ontology(lb_client)
    return spark_table

def __create_upload_data_row_values(row_data_col, global_key_col, external_id_col, metadata_name_key_to_schema_bytes):
    """ Function to-be-wrapped into a pyspark UDF that will create data row dict values (without metadata)
    Args:
        row_data_col                        :   Required (str) - Row data URL column name
        global_key_col                      :   Required (str) - Global Key colunmn name             
        external_id_col                     :   Required (str) - External ID column name
        metadata_name_key_to_schema_bytes   :   Required (bytes) - Bytearray representation of a dictionary where {key=metadata_field_name_key : value=metadata_schema_id}  
    Returns:
        Data row upload value as-a-dictionary with complete key/value pairs for "row_data", "external_id", and "global_key", and an empty list for key "metadata_fields"
    """
    metadata_name_key_to_schema = json.loads(metadata_name_key_to_schema_bytes)
    return {'row_data': row_data_col, 'external_id': external_id_col, 'global_key': global_key_col, 'metadata_fields': [{'schema_id': metadata_name_key_to_schema['lb_integration_source'], 'value': 'Databricks'}]}

def get_metadata_schema_to_name_key(lb_mdo: labelbox.schema.data_row_metadata.DataRowMetadataOntology.divider='///', invert=False):
    """ Creates a dictionary where {key=metadata_schema_id: value=metadata_name_key} 
    - name_key is name for all metadata fields, and for enum options, it is "parent_name{divider}child_name"
    Args:
        lb_mdo              :   Required (labelbox.schema.data_row_metadata.DataRowMetadataOntology) - Labelbox metadata ontology
        divider             :   Optional (str) - String separating parent and enum option metadata values
        invert              :   Optional (bool) - If True, will make the name_key the dictionary key and the schema_id the dictionary value
    Returns:
        Dictionary where {key=metadata_schema_id: value=metadata_name_key}
    """
    lb_metadata_dict = lb_mdo.reserved_by_name
    lb_metadata_dict.update(lb_mdo.custom_by_name)
    metadata_schema_to_name_key = {}
    for metadata_field_name_key in lb_metadata_dict:
        if type(lb_metadata_dict[metadata_field_name_key]) == dict:
            metadata_schema_to_name_key[lb_metadata_dict[metadata_field_name_key][next(iter(lb_metadata_dict[metadata_field_name_key]))].parent] = str(metadata_field_name_key)
            for enum_option in lb_metadata_dict[metadata_field_name_key]:
                metadata_schema_to_name_key[lb_metadata_dict[metadata_field_name_key][enum_option].uid] = f'{str(metadata_field_name_key)}{str(divider)}{str(enum_option)}'
        else:
            metadata_schema_to_name_key[lb_metadata_dict[metadata_field_name_key].uid] = str(metadata_field_name_key)
    return_value = metadata_schema_to_name_key if not invert else {v: k for (k, v) in metadata_schema_to_name_key.items()}
    return return_value

def attach_metadata_to_data_row_values(metadata_value_col, data_row_col, metadata_field_name_key, metadata_name_key_to_schema_bytes, metadata_index_bytes):
    """ Function to-be-wrapped into a pyspark UDF that will add a single metadata field / value pair to data row dict metdata lists
    Args:
        metadata_value_col                  :   Required (str) - Metadata value column name
        data_row_col                        :   Required (str) - Data Row Upload column name
        metadata_field_name_key             :   Required (str) - Metadata field name
        metadata_name_key_to_schema_bytes   :   Required (bytes) - Bytearray representation of a converter dictionary where {key=metadata_field_name_key : value=metadata_schema_id}  
        metadata_index_bytes                :   Required (bytes) - Bytearray representation of a converter dictionary where {key=metadata_field_name_key : value=metadata_type} - metadata_type must be one of "enum", "string", "datetime" or "number"
    Returns:
        Data row upload as-a-dictionary
    """
    metadata_name_to_schema = json.loads(metadata_name_key_to_schema_bytes)
    metadata_type = json.loads(metadata_index_bytes)[str(metadata_field_name_key)]
    if metadata_value_col is not None or str(metadata_value_col) != '':
        input_metadata_value = metadata_value_col if metadata_type != 'enum' else metadata_name_to_schema[str(metadata_value_col)]
        data_row['metadata_fields'].append({'schema_id': metadata_name_to_schema[str(metadata_field_name_key)], 'value': input_metadata_value})
    return data_row

def create_uploads_column(lb_client, spark_table, row_data_col, global_key_col, external_id_col, metadata_index={}):
    """ Creates a spark table with an "uploads" that can be queried and uploaded to Labebox
    Args:
        lb_client           :   Required (labelbox.Client) - Labelbox Clinet object    
        spark_table         :   Required (pyspark.sql.dataframe.Dataframe) - Spark Table
        row_data_col        :   Required (str) - Column name for the data row row data URL
        global_key_col      :   Required (str) - Column name for the global key
        external_id_col     :   Required (str) - Column name for the external ID
        metadata_index      :   Optional (dict) - Dictionary where {key=column_name : value=metadata_type} - metadata_type must be one of "enum", "string", "datetime" or "number"
    Returns:
        Updated version of the input `spark_table` with an `uploads` column which includes "row_data", "external_id", "global_key" and "metadata_fields"
    Uses:
        __create_upload_data_row_values
        attach_metadata_to_data_row_values
    """
    upload_schema = StructType([StructField('row_data', StringType()), StructField('global_key', StringType()), StructField('external_id', StringType()), StructField('metadata_fields', ArrayType(MapType(StringType(), StringType(), True)))])
    metadata_name_key_to_schema = get_metadata_schema_to_name_key(self.lb_client.get_data_row_metadata_ontology(), invert=True)
    data_row_udf = udf(__create_upload_data_row_values, upload_schema)
    df = spark_dataframe.withColumn('uploads', data_row_udf(row_data_col=row_data_col, global_key=global_key_col, external_id=external_id_col, metadata_name_key_to_schema_bytes=lit(json.dumps(metadata_name_key_to_schema))))
    if metadata_index:
        metadata_udf = udf(attach_metadata_to_data_row_values, upload_schema)
        for column_name in metadata_index:
            df = df.withColumn('uploads', metadata_udf(metadata_value_col=column_name, data_row_col='uploads', metadata_field_name_key=lit(column_name), metadata_name_key_to_schema_bytes=lit(json.dumps(metadata_name_key_to_schema)), metadata_index_bytes=lit(json.dumps(metadata_index))))
    return df

def batch_create_data_rows(client, dataset, global_key_to_upload_dict, skip_duplicates=True, batch_size=20000):
    """ Checks to make sure no duplicate global keys are uploaded before batch uploading data rows
    Args:
        client                      : Required (labelbox.client.Client) : Labelbox Client object
        dataset                     : Required (labelbox.dataset.Dataset) : Labelbox Dataset object
        global_key_to_upload_dict   : Required (dict) : Dictionary where {key=global_key : value=data_row_dict to-be-uploaded to Labelbox}
        skip_duplicates             : Optional (bool) - If True, will skip duplicate global_keys, otherwise will generate a unique global_key with a suffix "_1", "_2" and so on
        batch_size                  : Optional (int) : Upload batch size, 20,000 is recommended
    Returns:
        A concatenated list of upload results for all batch uploads
    """

    def __check_global_keys(client, global_keys):
        """ Checks if data rows exist for a set of global keys
        Args:
            client                  : Required (labelbox.client.Client) : Labelbox Client object
            global_keys             : Required (list(str)) : List of global key strings
        Returns:
            True if global keys are available, False if not
        """
        query_keys = [str(x) for x in global_keys]
        query_str_1 = 'query get_datarow_with_global_key($global_keys:[ID!]!){dataRowsForGlobalKeys(where:{ids:$global_keys}){jobId}}'
        query_job_id = client.execute(query_str_1, {'global_keys': global_keys})['dataRowsForGlobalKeys']['jobId']
        query_str_2 = 'query get_job_result($job_id:ID!){dataRowsForGlobalKeysResult(jobId:{id:$job_id}){data{\n                        accessDeniedGlobalKeys\ndeletedDataRowGlobalKeys\nfetchedDataRows{id}\nnotFoundGlobalKeys}jobStatus}}'
        res = client.execute(query_str_2, {'job_id': query_job_id})['dataRowsForGlobalKeysResult']['data']
        return res
    global_keys_list = list(global_key_to_upload_dict.keys())
    payload = __check_global_keys(client, global_keys_list)
    loop_counter = 0
    if payload:
        while len(payload['notFoundGlobalKeys']) != len(global_keys_list):
            if payload['deletedDataRowGlobalKeys']:
                client.clear_global_keys(payload['deletedDataRowGlobalKeys'])
                payload = __check_global_keys(client, global_keys_list)
                continue
            if payload['fetchedDataRows']:
                loop_counter += 1
                for i in range(0, len(payload['fetchedDataRows'])):
                    global_key = str(global_keys_list[i]).split('_')[0] if loop_counter >= 2 else str(global_keys_list[i])
                    new_global_key = f'{global_key}_{loop_counter}'
                    if payload['fetchedDataRows'][i] != '':
                        if skip_duplicates:
                            del global_key_to_upload_dict[global_key]
                        else:
                            new_upload_dict = global_key_to_upload_dict[global_key]
                            del global_key_to_upload_dict[global_key]
                            new_upload_dict['global_key'] = new_global_key
                            global_key_to_upload_dict[new_global_key] = new_upload_dict
                global_keys_list = list(global_key_to_upload_dict.keys())
                payload = __check_global_keys(client, global_keys_list)
    upload_list = list(global_key_to_upload_dict.values())
    upload_results = []
    for i in range(0, len(upload_list), batch_size):
        batch = upload_list[i:] if i + batch_size >= len(upload_list) else upload_list[i:i + batch_size]
        task = dataset.create_data_rows(batch)
        errors = task.errors
        if errors:
            print(f'Data Row Creation Error: {errors}')
            return errors
        else:
            upload_results.extend(task.result)
    return upload_results

def upsert_function(upsert_dict_bytes, global_key_col, metadata_value_col):
    """ Nested UDF Functionality upsert metadata in Labelbox and in the pyspark dataframe
    Args:  
        upsert_dict_bytes               :   Required (bytes) - Bytearray representation of a converter dictionary where {key=global_keys and value=latest_metadata_values}
        global_key_col                  :   Required (str) - Column name for the global_key
        metadata_value_col              :   Required (str) - Column name for the  current metadata value
    Returns:
        New value to-be-inserted in the column corresponding to this metadata field
    """
    upsert_dict = json.loads(upsert_dict_bytes)
    if global_key_col in upsert_dict.keys():
        return_value = upsert_dict[global_key_col]
    else:
        return_value = metadata_value_col
    return return_value

def metadata_upsert_udf():
    """ Returns a UDF that will upsert a column given a dictionary where {key=column_name : value=new_value}
    Returns:
        UDF object to-be-run using: spark_dataframe.withColumn(col_name, udf(**kwargs))
    """
    return udf(upsert_function(), StringType())