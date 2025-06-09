from __future__ import absolute_import, division, print_function
__metaclass__ = type
import abc
from ansible.errors import AnsibleError
from ansible.module_utils import six
from ansible.module_utils.common._collections_compat import Sequence
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible.template import Templar
from ansible_collections.community.dns.plugins.module_utils.provider import ensure_type
from ansible_collections.community.dns.plugins.module_utils.zone_record_api import DNSAPIError, DNSAPIAuthenticationError
from ansible_collections.community.dns.plugins.module_utils.conversion.base import DNSConversionError
from ansible_collections.community.dns.plugins.module_utils.conversion.converter import RecordConverter
display = Display()

@six.add_metaclass(abc.ABCMeta)
class RecordsInventoryModule(BaseInventoryPlugin):
    VALID_ENDINGS = ('dns.yaml', 'dns.yml')

    def __init__(self):
        super(RecordsInventoryModule, self).__init__()

    @abc.abstractmethod
    def setup_api(self):
        """
        This function needs to set up self.provider_information and self.api.
        It can indicate errors by raising DNSAPIError.
        """

    def verify_file(self, path):
        if super(RecordsInventoryModule, self).verify_file(path):
            if path.endswith(self.VALID_ENDINGS):
                return True
            else:
                display.debug('{name} inventory filename must end with {endings}'.format(name=self.NAME, endings=' or '.join(["'{0}'".format(ending) for ending in self.VALID_ENDINGS])))
        return False

    def parse(self, inventory, loader, path, cache=False):
        super(RecordsInventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)
        self.templar = Templar(loader=loader)
        try:
            self.setup_api()
            self.record_converter = RecordConverter(self.provider_information, self)
            self.record_converter.emit_deprecations(display.deprecated)
            zone_name = self.get_option('zone_name')
            if self.templar.is_template(zone_name):
                zone_name = self.templar.template(variable=zone_name, disable_lookups=False)
            zone_id = self.get_option('zone_id')
            if zone_id is not None:
                if self.templar.is_template(zone_id):
                    zone_id = self.templar.template(variable=zone_id, disable_lookups=False)
                zone_id_type = self.provider_information.get_record_id_type()
                try:
                    zone_id = ensure_type(zone_id, zone_id_type)
                except TypeError as exc:
                    raise AnsibleError(u'Error while ensuring that zone_id is of type {0}: {1}'.format(zone_id_type, exc))
            if zone_name is not None:
                zone_with_records = self.api.get_zone_with_records_by_name(zone_name)
            elif zone_id is not None:
                zone_with_records = self.api.get_zone_with_records_by_id(zone_id)
            else:
                raise AnsibleError('One of zone_name and zone_id must be specified!')
            if zone_with_records is None:
                raise AnsibleError('Zone does not exist')
            self.record_converter.process_multiple_from_api(zone_with_records.records)
            self.record_converter.process_multiple_to_user(zone_with_records.records)
        except DNSConversionError as e:
            raise AnsibleError(u'Error while converting DNS values: {0}'.format(e.error_message))
        except DNSAPIAuthenticationError as e:
            raise AnsibleError('Cannot authenticate: %s' % e)
        except DNSAPIError as e:
            raise AnsibleError('Error: %s' % e)
        filters = self.get_option('filters')
        filter_types = filters.get('type') or ['A', 'AAAA', 'CNAME']
        if not isinstance(filter_types, Sequence) or isinstance(filter_types, six.string_types):
            filter_types = [filter_types]
        for record in zone_with_records.records:
            if record.type in filter_types:
                name = zone_with_records.zone.name
                if record.prefix:
                    name = '%s.%s' % (record.prefix, name)
                self.inventory.add_host(name)
                self.inventory.set_variable(name, 'ansible_host', record.target)