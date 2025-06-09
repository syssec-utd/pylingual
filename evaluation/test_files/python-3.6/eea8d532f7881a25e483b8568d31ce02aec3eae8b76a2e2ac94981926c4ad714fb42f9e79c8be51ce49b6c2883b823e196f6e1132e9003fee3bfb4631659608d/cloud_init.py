"""
Custom datasources for cloud initialization information
"""
import yaml
from insights.core.context import HostContext
from insights.core.dr import SkipComponent
from insights.core.plugins import datasource
from insights.core.filters import get_filters
from insights.core.spec_factory import DatasourceProvider, simple_file
from insights.specs import Specs

class LocalSpecs(Specs):
    """ Local specs used only by cloud_init datasources """
    cloud_cfg_input = simple_file('/etc/cloud/cloud.cfg')
    ' Returns the contents of the file ``/etc/cloud/cloud.cfg`` '

@datasource(LocalSpecs.cloud_cfg_input, HostContext)
def cloud_cfg(broker):
    """
    This datasource provides configuration of ``/etc/cloud/cloud.cfg`` file.

    .. note::
        Since this file may contain sensitive information, it should be
        filtered before the Insights collecting it.  The filters will be added
        via the :mod:`insights.specs.Specs.cloud_cfg` Spec.  If nothing is
        added to the filter, nothing will be collected.

    Typical content of ``/etc/cloud/cloud.cfg`` file is::

        #cloud-config
        users:
          - name: demo
            ssh-authorized-keys:
              - key_one
              - key_two
            passwd: $6$j212wezy$7H/1LT4f9/N3wpgNunhsIqtMj62OKiS3nyNwuizouQc3u7

        ssh_deletekeys: 1

        network:
            version: 1
            config:
              - type: physical
                name: eth0
                subnets:
                  - type: dhcp
                  - type: dhcp6

        system_info:
            default_user:
            name: user2
            plain_text_passwd: 'someP@assword'
            home: /home/user2

        debug:
            output: /var/log/cloud-init-debug.log
            verbose: true

    Returns:
        str: YAML string after removing the sensitive information.

    Raises:
        SkipComponent: When the path does not exist, nothing is collected,
                       or any exception occurs.
    """
    relative_path = '/etc/cloud/cloud.cfg'
    try:
        filters = get_filters(Specs.cloud_cfg)
        content = broker[LocalSpecs.cloud_cfg_input].content
        if content and filters:
            result = dict()
            content = yaml.load('\n'.join(content), Loader=yaml.SafeLoader)
            if isinstance(content, dict):
                for item in filters:
                    if item not in ('users', 'system_info') and item in content:
                        result[item] = content[item]
                if result:
                    return DatasourceProvider(content=yaml.dump(result), relative_path=relative_path)
            raise SkipComponent('Invalid YAML format')
    except Exception as e:
        raise SkipComponent('Unexpected exception:{e}'.format(e=str(e)))
    raise SkipComponent