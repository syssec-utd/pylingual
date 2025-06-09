import os
import inspect
import tempfile
import unified_planning
from unified_planning.shortcuts import *
from unified_planning.test import TestCase, skipIfEngineNotAvailable

class TestFactory(TestCase):

    @skipIfEngineNotAvailable('pyperplan')
    @skipIfEngineNotAvailable('tamer')
    def test_config_file(self):
        self.assertTrue('pyperplan' in get_env().factory.preference_list)
        with tempfile.TemporaryDirectory() as tempdir:
            config_filename = os.path.join(tempdir, 'up.ini')
            with open(config_filename, 'w') as config:
                config.write('[global]\n')
                config.write('engine_preference_list: tamer\n')
            env = unified_planning.environment.Environment()
            env.factory.configure_from_file(config_filename)
            self.assertTrue('pyperplan' not in env.factory.preference_list)
            self.assertEqual(env.factory.preference_list, ['tamer'])