from pathlib import Path
from tests.plugins import PluginTestCase
from troubadix.plugin import LinterWarning
from troubadix.plugins.script_calls_recommended import CheckScriptCallsRecommended

class CheckScriptCallsRecommendedTestCase(PluginTestCase):
    path = Path('some/file.nasl')

    def test_ok(self):
        content = 'script_dependencies();\nscript_require_ports();\nscript_require_udp_ports();\nscript_require_keys();\nscript_mandatory_keys();'
        fake_context = self.create_file_plugin_context(nasl_file=self.path, file_content=content)
        plugin = CheckScriptCallsRecommended(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 0)

    def test_exclude_inc_file(self):
        path = Path('some/file.inc')
        fake_context = self.create_file_plugin_context(nasl_file=path)
        plugin = CheckScriptCallsRecommended(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 0)

    def test_missing_calls(self):
        content = 'script_xref(name: "URL", value:"");'
        fake_context = self.create_file_plugin_context(nasl_file=self.path, file_content=content)
        plugin = CheckScriptCallsRecommended(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], LinterWarning)

    def test_dependencies_multiline(self):
        content = 'script_dependencies("123",\n"456");\nscript_require_ports();\nscript_require_udp_ports();\nscript_require_keys();\nscript_mandatory_keys();'
        fake_context = self.create_file_plugin_context(nasl_file=self.path, file_content=content)
        plugin = CheckScriptCallsRecommended(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 0)