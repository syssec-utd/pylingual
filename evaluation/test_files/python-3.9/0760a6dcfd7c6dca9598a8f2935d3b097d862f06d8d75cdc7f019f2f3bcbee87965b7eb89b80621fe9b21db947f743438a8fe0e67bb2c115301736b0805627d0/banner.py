from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.utils.display import Display
from ansible_collections.ansible.netcommon.plugins.action.network import ActionModule as ActionNetworkModule
display = Display()

class ActionModule(ActionNetworkModule):

    def run(self, tmp=None, task_vars=None):
        del tmp
        module_name = self._task.action.split('.')[-1]
        self._config_module = True if module_name in ['ios_config', 'config'] else False
        persistent_connection = self._play_context.connection.split('.')[-1]
        warnings = []
        if persistent_connection != 'network_cli':
            return {'failed': True, 'msg': 'Connection type %s is not valid for this module' % self._play_context.connection}
        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if 'warnings' in result:
                result['warnings'].extend(warnings)
            else:
                result['warnings'] = warnings
        return result