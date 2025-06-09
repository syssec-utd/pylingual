import logging
import os
import shutil
import unittest
import peek_platform
from jsoncfg.functions import config_to_json_str
from peek_platform.file_config.PeekFileConfigABC import PeekFileConfigABC
from peek_platform.file_config.PeekFileConfigDataExchangeClientMixin import PeekFileConfigDataExchangeClientMixin
from peek_platform.file_config.PeekFileConfigPlatformMixin import PeekFileConfigPlatformMixin
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestFileConfig(PeekFileConfigABC, PeekFileConfigDataExchangeClientMixin, PeekFileConfigPlatformMixin):
    pass

class PeekFileConfigTest(unittest.TestCase):
    COMPONENT_NAME = 'unit_test'
    HOME_DIR = os.path.expanduser('~/%s.home' % COMPONENT_NAME)
    CONFIG_FILE_PATH = os.path.join(HOME_DIR, 'config.json')

    def _rmHome(self):
        if os.path.exists(self.HOME_DIR):
            shutil.rmtree(self.HOME_DIR)

    def setUp(self):
        TestFileConfig._PeekFileConfigBase__instance = None
        peek_platform.PeekPlatformConfig.componentName = 'unit_test'
        self._rmHome()
        os.makedirs(self.HOME_DIR, TestFileConfig.DEFAULT_DIR_CHMOD)
        with open(self.CONFIG_FILE_PATH, 'w') as fobj:
            fobj.write('{"nothing":{"is_true":true}}')

    def tearDown(self):
        self._rmHome()

    def testReadingConfig(self):
        bas = TestFileConfig()
        logger.info('nothing.is_true = %s', bas._cfg.nothing.is_true)
        self.assertTrue(bas._cfg.nothing.is_true())

    def testPeekServerDetails(self):
        bas = TestFileConfig()
        logger.info('peekServerPort = %s', bas.peekServerPort)
        logger.info('peekServerHost = %s', bas.peekServerHost)
        logger.info(config_to_json_str(bas._cfg))
        bas._save()
        with open(self.CONFIG_FILE_PATH, 'r') as fobj:
            logger.info(fobj.read())

    def testAsignment(self):
        inArr = [1, 2, 5, '20']
        valuey = 'valuey'
        twoFiveSix = 256
        bas = TestFileConfig()
        bas._cfg.op1.thingx = valuey
        bas._cfg.op1.thingy = twoFiveSix
        bas._cfg.op2.op3.arr = inArr
        logger.info(config_to_json_str(bas._cfg))
        bas._save()
        with open(self.CONFIG_FILE_PATH, 'r') as fobj:
            logger.info(fobj.read())
        TestFileConfig._PeekFileConfigBase__instance = None
        bas = TestFileConfig()
        self.assertEqual(bas._cfg.op2.op3.arr(), inArr)
        self.assertEqual(bas._cfg.op1.thingx(), valuey)
        self.assertEqual(bas._cfg.op1.thingy(), twoFiveSix)

    def testPlatformDetails(self):
        pluginName = 'plugin_noop'
        bas = TestFileConfig()
        logger.info('plugin.plugin_noop.version = %s', bas.pluginVersion(pluginName))
        logger.info('platformVersion = %s', bas.platformVersion)
        bas.platformVersion = '4.4.4'
        bas.setPluginVersion(pluginName, '2.5.6')
        with open(self.CONFIG_FILE_PATH, 'r') as fobj:
            logger.info(fobj.read())
        TestFileConfig._PeekFileConfigBase__instance = None
        logger.info('plugin.plugin_noop.version = %s', bas.pluginVersion(pluginName))
        logger.info('platformVersion = %s', bas.platformVersion)
        self.assertEqual(bas.platformVersion, '4.4.4')
        self.assertEqual(bas.pluginVersion(pluginName), '2.5.6')