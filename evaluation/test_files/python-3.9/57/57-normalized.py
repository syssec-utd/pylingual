def _get_aws_credentials(self):
    """
        returns aws_access_key_id, aws_secret_access_key
        from extra

        intended to be used by external import and export statements
        """
    if self.snowflake_conn_id:
        connection_object = self.get_connection(self.snowflake_conn_id)
        if 'aws_secret_access_key' in connection_object.extra_dejson:
            aws_access_key_id = connection_object.extra_dejson.get('aws_access_key_id')
            aws_secret_access_key = connection_object.extra_dejson.get('aws_secret_access_key')
    return (aws_access_key_id, aws_secret_access_key)