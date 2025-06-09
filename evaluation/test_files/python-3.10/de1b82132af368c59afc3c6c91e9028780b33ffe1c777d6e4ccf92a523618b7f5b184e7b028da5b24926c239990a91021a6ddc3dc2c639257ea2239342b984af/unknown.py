"""Module used to define a generic unknown event."""
import json
import base64
import uuid
from faassupervisor.utils import SysUtils, FileUtils

class UnknownEvent:
    """Class to manage unknown events."""
    _TYPE = 'UNKNOWN'

    def __init__(self, event):
        self._file_name = 'event-file-{}'.format(str(uuid.uuid4()))
        self.event = event
        if isinstance(event, dict):
            records = event.get('Records')
            if records:
                self.event_records = records[0]
        self._set_event_params()

    def _set_event_params(self):
        """ Generic method to be implemented by all the event parsers. """

    def get_type(self):
        """Returns the event type.
        Default event is UNKNOWN, but it can also
        be APIGATEWAY, MINIO, ONEDATA, and S3.

        Each class inheriting from UnkownEvent
        must override the _TYPE."""
        return self._TYPE

    def save_event(self, input_dir_path):
        """Stores the unknown event and returns
        the file path where the file is stored."""
        file_path = SysUtils.join_paths(input_dir_path, self._file_name)
        try:
            json.loads(self.event)
        except ValueError:
            FileUtils.create_file_with_content(file_path, base64.b64decode(self.event), mode='wb')
        except TypeError:
            FileUtils.create_file_with_content(file_path, self.event)
        else:
            FileUtils.create_file_with_content(file_path, self.event)
        return file_path