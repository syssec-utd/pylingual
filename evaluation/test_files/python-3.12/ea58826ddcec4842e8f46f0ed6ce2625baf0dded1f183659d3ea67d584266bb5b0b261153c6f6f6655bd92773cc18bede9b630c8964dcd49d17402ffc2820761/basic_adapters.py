import json
from typing import Union
from th2.data_services.interfaces.adapter import IRecordAdapter
from google.protobuf.json_format import MessageToDict
from th2_grpc_lw_data_provider.lw_data_provider_pb2 import EventResponse, MessageGroupResponse

class GRPCObjectToDictAdapter(IRecordAdapter):
    """GRPC Adapter decodes a GRPC object into a Dict object."""

    def handle(self, record: Union[MessageGroupResponse, EventResponse]) -> dict:
        """Decodes MessageGroupResponse or EventResponse as GRPC object into a Dict object.

        Args:
            record: MessageGroupResponse/EventResponse.

        Returns:
            Dict object.
        """
        new_record = MessageToDict(record, including_default_value_fields=True)
        if isinstance(record, EventResponse):
            new_record['startTimestamp'] = {'epochSecond': record.start_timestamp.seconds, 'nano': record.start_timestamp.nanos}
            new_record['endTimestamp'] = {'epochSecond': record.end_timestamp.seconds, 'nano': record.end_timestamp.nanos}
            if 'batchId' not in new_record:
                new_record['batchId'] = None
            if 'parentEventId' not in new_record:
                new_record['parentEventId'] = None
        elif isinstance(record, MessageGroupResponse):
            new_record['timestamp'] = {'epochSecond': record.timestamp.seconds, 'nano': record.timestamp.nanos}
        try:
            new_record['body'] = json.loads(record.body)
        except (KeyError, AttributeError, json.JSONDecodeError):
            return new_record
        except Exception as e:
            raise Exception(f'{e}; Current record: {record}')
        return new_record