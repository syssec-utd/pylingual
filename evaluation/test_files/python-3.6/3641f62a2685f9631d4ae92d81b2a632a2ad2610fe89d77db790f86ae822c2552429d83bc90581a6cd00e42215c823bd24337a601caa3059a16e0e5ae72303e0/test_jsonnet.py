import json
import os
import re
import unittest
from io import StringIO
from jsonargparse import ActionConfigFile, ActionJsonnet, ActionJsonnetExtVars, ActionJsonSchema, ArgumentParser, strip_meta, ParserError
from jsonargparse.optionals import jsonnet_support
from jsonargparse_tests.base import TempDirTestCase
example_1_jsonnet = "\nlocal make_record(num) = {\n    'ref': '#'+(num+1),\n    'val': 3*(num/2)+5,\n};\n\n{\n  'param': 654,\n  'records': [make_record(n) for n in std.range(0, 8)],\n}\n"
example_2_jsonnet = "\nlocal param = std.extVar('param');\n\nlocal make_record(num) = {\n    'ref': '#'+(num+1),\n    'val': 3*(num/2)+5,\n};\n\n{\n  'param': param,\n  'records': [make_record(n) for n in std.range(0, 8)],\n}\n"
records_schema = {'type': 'array', 'items': {'type': 'object', 'properties': {'ref': {'type': 'string'}, 'val': {'type': 'number'}}}}
example_schema = {'type': 'object', 'properties': {'param': {'type': 'integer'}, 'records': records_schema}}

@unittest.skipIf(not jsonnet_support, 'jsonnet and jsonschema packages are required')
class JsonnetTests(TempDirTestCase):

    def test_parser_mode_jsonnet(self):
        parser = ArgumentParser(parser_mode='jsonnet', error_handler=None)
        parser.add_argument('--cfg', action=ActionConfigFile)
        parser.add_argument('--param', type=int)
        parser.add_argument('--records', action=ActionJsonSchema(schema=records_schema))
        jsonnet_file = os.path.join(self.tmpdir, 'example.jsonnet')
        with open(jsonnet_file, 'w') as output_file:
            output_file.write(example_1_jsonnet)
        cfg = parser.parse_args(['--cfg', jsonnet_file])
        self.assertEqual(654, cfg.param)
        self.assertEqual(9, len(cfg.records))
        self.assertEqual('#8', cfg.records[-2]['ref'])
        self.assertEqual(15.5, cfg.records[-2]['val'])
        self.assertRaises(ParserError, lambda : parser.parse_args(['--cfg', '{}}']))

    def test_parser_mode_jsonnet_import_issue_122(self):
        os.mkdir('conf')
        with open(os.path.join('conf', 'name.libsonnet'), 'w') as f:
            f.write('"Mike"')
        config_path = os.path.join('conf', 'test.jsonnet')
        with open(config_path, 'w') as f:
            f.write('local name = import "name.libsonnet"; {"name": name, "prize": 80}')
        parser = ArgumentParser(parser_mode='jsonnet')
        parser.add_argument('--cfg', action=ActionConfigFile)
        parser.add_argument('--name', type=str, default='Lucky')
        parser.add_argument('--prize', type=int, default=100)
        cfg = parser.parse_args([f'--cfg={config_path}'])
        self.assertEqual(cfg.name, 'Mike')
        self.assertEqual(cfg.prize, 80)
        self.assertEqual(str(cfg.cfg[0]), config_path)

    def test_parser_mode_jsonnet_subconfigs_issue_125(self):
        os.mkdir('conf')
        with open(os.path.join('conf', 'name.libsonnet'), 'w') as f:
            f.write('"Mike"')
        config_path = os.path.join('conf', 'test.jsonnet')
        with open(config_path, 'w') as f:
            f.write('local name = import "name.libsonnet"; {"name": name, "prize": 80}')

        class Class:

            def __init__(self, name: str='Lucky', prize: int=100):
                pass
        parser = ArgumentParser(parser_mode='jsonnet', error_handler=None)
        parser.add_class_arguments(Class, 'group', sub_configs=True)
        cfg = parser.parse_args([f'--group={config_path}'])
        self.assertEqual(cfg.group.name, 'Mike')
        self.assertEqual(cfg.group.prize, 80)

    def test_ActionJsonnet(self):
        parser = ArgumentParser(default_meta=False, error_handler=None)
        parser.add_argument('--input.ext_vars', action=ActionJsonnetExtVars())
        parser.add_argument('--input.jsonnet', action=ActionJsonnet(ext_vars='input.ext_vars', schema=json.dumps(example_schema)))
        cfg2 = parser.parse_args(['--input.ext_vars', '{"param": 123}', '--input.jsonnet', example_2_jsonnet])
        self.assertEqual(123, cfg2.input.jsonnet['param'])
        self.assertEqual(9, len(cfg2.input.jsonnet['records']))
        self.assertEqual('#8', cfg2.input.jsonnet['records'][-2]['ref'])
        self.assertEqual(15.5, cfg2.input.jsonnet['records'][-2]['val'])
        cfg1 = parser.parse_args(['--input.jsonnet', example_1_jsonnet])
        self.assertEqual(cfg1.input.jsonnet['records'], cfg2.input.jsonnet['records'])
        self.assertRaises(ParserError, lambda : parser.parse_args(['--input.ext_vars', '{"param": "a"}', '--input.jsonnet', example_2_jsonnet]))
        self.assertRaises(ParserError, lambda : parser.parse_args(['--input.jsonnet', example_2_jsonnet]))
        self.assertRaises(ValueError, lambda : ActionJsonnet(ext_vars=2))
        self.assertRaises(ValueError, lambda : ActionJsonnet(schema='.' + json.dumps(example_schema)))

    def test_ActionJsonnet_save(self):
        parser = ArgumentParser(error_handler=None)
        parser.add_argument('--ext_vars', action=ActionJsonnetExtVars())
        parser.add_argument('--jsonnet', action=ActionJsonnet(ext_vars='ext_vars'))
        parser.add_argument('--cfg', action=ActionConfigFile)
        jsonnet_file = os.path.join(self.tmpdir, 'example.jsonnet')
        with open(jsonnet_file, 'w') as output_file:
            output_file.write(example_2_jsonnet)
        outdir = os.path.join(self.tmpdir, 'output')
        outyaml = os.path.join(outdir, 'main.yaml')
        outjsonnet = os.path.join(outdir, 'example.jsonnet')
        os.mkdir(outdir)
        cfg = parser.parse_args(['--ext_vars', '{"param": 123}', '--jsonnet', jsonnet_file])
        self.assertEqual(str(cfg.jsonnet['__path__']), jsonnet_file)
        parser.save(cfg, outyaml)
        cfg2 = parser.parse_args(['--cfg', outyaml])
        cfg2.cfg = None
        self.assertTrue(os.path.isfile(outyaml))
        self.assertTrue(os.path.isfile(outjsonnet))
        self.assertEqual(strip_meta(cfg), strip_meta(cfg2))
        os.unlink(outyaml)
        os.unlink(outjsonnet)
        parser.save(strip_meta(cfg), outyaml)
        cfg3 = parser.parse_args(['--cfg', outyaml])
        cfg3.cfg = None
        self.assertTrue(os.path.isfile(outyaml))
        self.assertTrue(not os.path.isfile(outjsonnet))
        self.assertEqual(strip_meta(cfg), strip_meta(cfg3))

    def test_ActionJsonnet_help(self):
        parser = ArgumentParser()
        parser.add_argument('--jsonnet', action=ActionJsonnet(schema=example_schema), help='schema: %s')
        out = StringIO()
        parser.print_help(out)
        outval = out.getvalue()
        schema = re.sub('^.*schema:([^()]+)[^{}]*$', '\\1', outval.replace('\n', ' '))
        self.assertEqual(example_schema, json.loads(schema))

    def test_ActionJsonnet_parse(self):
        parser = ArgumentParser(error_handler=None)
        parser.add_argument('--ext_vars', action=ActionJsonnetExtVars())
        cfg = parser.parse_args(['--ext_vars', '{"param": 123}'])
        parsed = ActionJsonnet(schema=None).parse(example_2_jsonnet, ext_vars=cfg.ext_vars)
        self.assertEqual(123, parsed['param'])
        self.assertEqual(9, len(parsed['records']))
        self.assertEqual('#8', parsed['records'][-2]['ref'])
        self.assertEqual(15.5, parsed['records'][-2]['val'])
        cfg2 = parser.parse_object({'ext_vars': {'param': 123}})
        self.assertEqual(cfg.ext_vars, cfg2.ext_vars)
if __name__ == '__main__':
    unittest.main(verbosity=2)