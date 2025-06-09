""" Module w.r.t. Azure table storage logic."""
import pandas as pd
from azure.data.tables import TableClient
from warpzone.tablestorage import data
from warpzone.tablestorage.operations import TableOperations

class WarpzoneTableClient:
    """Class to interact with Azure Table"""

    def __init__(self, table_client: TableClient):
        self._table_client = table_client
        self.table_name = table_client.table_name

    @classmethod
    def from_connection_string(cls, conn_str: str, table_name: str):
        """Get table client from connection string

        Args:
            conn_str (str): Connection string to table service
            table_name (str): Name of table
        """
        table_client = TableClient.from_connection_string(conn_str, table_name)
        return cls(table_client)

    def execute_table_operations(self, operations: TableOperations):
        """Perform table storage operations from a operation set.

        Args:
            operations (TableOperations): Iterable of lists of table operations (dicts)
        """
        for batch in operations:
            self._table_client.submit_transaction(batch)

    def query(self, query: str) -> list[dict]:
        """Retrieve data from Table Storage using linq query

        Args:
            query (str): Linq query.

        Returns:
            typing.List[typing.Dict]: List of entities.
        """
        entities = [record for record in self._table_client.query_entities(query)]
        return entities

    def query_partition(self, partition_key: str) -> list[dict]:
        """Retrieve data from Table Storage using partition key

        Args:
            partition_key (str): Partion key.

        Returns:
            typing.List[typing.Dict]: List of entities.
        """
        query = f"PartitionKey eq '{partition_key}'"
        return self.query(query)

    def read_pandas(self, query: str='', keep_keys: bool=False) -> pd.DataFrame:
        """Read pandas dataframe from the table storage

        Args:
            query (str, optional): Linq query. Defaults to "".
            keep_keys (bool, optional): Keep columns `PartitionKey` and `RowKey`.
                Defaults to False.
        """
        entities = self.query(query)
        if len(entities) == 0:
            return pd.DataFrame()
        return data.entities_to_pandas(entities, keep_keys)

    def write_pandas(self, df: pd.DataFrame, partition_keys: list[str], row_keys: list[str], operation_type: str):
        """Write pandas dataframe to table storage

        Args:
            df (pd.DataFrame): Pandas dataframe
            partition_keys (list[str]): Partition key columns
            row_keys (list[str]): Row key columns
            operation_type (str): Operation type
        """
        table_operations = data.pandas_to_table_operations(df, partition_keys, row_keys, operation_type)
        self.execute_table_operations(table_operations)