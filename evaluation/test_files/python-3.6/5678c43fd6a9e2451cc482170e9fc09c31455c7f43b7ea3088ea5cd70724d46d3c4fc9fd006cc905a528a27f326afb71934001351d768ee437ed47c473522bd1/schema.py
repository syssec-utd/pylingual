from __future__ import annotations
from typing import Optional
from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.client.data_classes import TransformationDestination, TransformationSchemaColumn, TransformationSchemaColumnList
from cognite.client.data_classes.transformations.common import DataModelInstances

class TransformationSchemaAPI(APIClient):
    _RESOURCE_PATH = '/transformations/schema'

    def retrieve(self, destination: TransformationDestination, conflict_mode: Optional[str]=None) -> TransformationSchemaColumnList:
        """`Get expected schema for a transformation destination. <https://docs.cognite.com/api/v1/#operation/getTransformationSchema>`_

        Args:
            destination (TransformationDestination): destination for which the schema is requested.
            conflict_mode (Optional[str]): conflict mode for which the schema is requested.

        Returns:
            TransformationSchemaColumnList: List of column descriptions

        Example:

            Get the schema for a transformation producing assets::

                >>> from cognite.client import CogniteClient
                >>> from cognite.client.data_classes import TransformationDestination
                >>> c = CogniteClient()
                >>> columns = c.transformations.schema.retrieve(destination = TransformationDestination.assets())
        """
        url_path = utils._auxiliary.interpolate_and_url_encode(self._RESOURCE_PATH + '/{}', str(destination.type))
        filter = destination.dump(True)
        filter.pop('type')
        if isinstance(destination, DataModelInstances):
            filter['externalId'] = filter.pop('modelExternalId')
            filter.pop('instanceSpaceExternalId')
        if conflict_mode:
            filter['conflictMode'] = conflict_mode
        return self._list(list_cls=TransformationSchemaColumnList, resource_cls=TransformationSchemaColumn, method='GET', resource_path=url_path, filter=filter)