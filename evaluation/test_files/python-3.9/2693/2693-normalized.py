def create_database(self, server_name, name, service_objective_id, edition=None, collation_name=None, max_size_bytes=None):
    """
        Creates a new Azure SQL Database.

        server_name:
            Name of the server to contain the new database.
        name:
            Required. The name for the new database. See Naming Requirements
            in Azure SQL Database General Guidelines and Limitations and
            Database Identifiers for more information.
        service_objective_id:
            Required. The GUID corresponding to the performance level for
            Edition. See List Service Level Objectives for current values.
        edition:
            Optional. The Service Tier (Edition) for the new database. If
            omitted, the default is Web. Valid values are Web, Business,
            Basic, Standard, and Premium. See Azure SQL Database Service Tiers
            (Editions) and Web and Business Edition Sunset FAQ for more
            information.
        collation_name:
            Optional. The database collation. This can be any collation
            supported by SQL. If omitted, the default collation is used. See
            SQL Server Collation Support in Azure SQL Database General
            Guidelines and Limitations for more information.
        max_size_bytes:
            Optional. Sets the maximum size, in bytes, for the database. This
            value must be within the range of allowed values for Edition. If
            omitted, the default value for the edition is used. See Azure SQL
            Database Service Tiers (Editions) for current maximum databases
            sizes. Convert MB or GB values to bytes.
            1 MB = 1048576 bytes. 1 GB = 1073741824 bytes.
        """
    _validate_not_none('server_name', server_name)
    _validate_not_none('name', name)
    _validate_not_none('service_objective_id', service_objective_id)
    return self._perform_post(self._get_databases_path(server_name), _SqlManagementXmlSerializer.create_database_to_xml(name, service_objective_id, edition, collation_name, max_size_bytes))