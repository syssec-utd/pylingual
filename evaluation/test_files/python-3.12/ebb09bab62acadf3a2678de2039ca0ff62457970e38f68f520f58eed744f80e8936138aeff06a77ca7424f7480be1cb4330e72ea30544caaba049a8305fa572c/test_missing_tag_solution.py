from pathlib import Path
from troubadix.plugin import LinterError
from troubadix.plugins.missing_tag_solution import CheckMissingTagSolution
from . import PluginTestCase

class CheckDoubleEndPointsTestCase(PluginTestCase):

    def test_ok(self):
        path = Path('some/file.nasl')
        content = 'script_tag(name:"cvss_base", value:"4.0");\nscript_tag(name:"summary", value:"Foo Bar.");\nscript_tag(name:"solution_type", value:"VendorFix");\nscript_tag(name:"solution", value:"meh");\n'
        fake_context = self.create_file_plugin_context(nasl_file=path, file_content=content)
        plugin = CheckMissingTagSolution(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 0)

    def test_exclude_inc_file(self):
        path = Path('some/file.inc')
        fake_context = self.create_file_plugin_context(nasl_file=path)
        plugin = CheckMissingTagSolution(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 0)

    def test_no_solution_type(self):
        path = Path('some/file.nasl')
        content = 'script_tag(name:"cvss_base", value:"4.0");\nscript_tag(name:"summary", value:"Foo Bar...");'
        fake_context = self.create_file_plugin_context(nasl_file=path, file_content=content)
        plugin = CheckMissingTagSolution(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 0)

    def test_missing_solution(self):
        path = Path('some/file.nasl')
        content = 'script_tag(name:"cvss_base", value:"4.0");\nscript_tag(name:"summary", value:"Foo Bar...");script_tag(name:"solution_type", value:"VendorFix");\n'
        fake_context = self.create_file_plugin_context(nasl_file=path, file_content=content)
        plugin = CheckMissingTagSolution(fake_context)
        results = list(plugin.run())
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], LinterError)
        self.assertEqual("'solution_type' script_tag but no 'solution' script_tag found in the description block.", results[0].message)