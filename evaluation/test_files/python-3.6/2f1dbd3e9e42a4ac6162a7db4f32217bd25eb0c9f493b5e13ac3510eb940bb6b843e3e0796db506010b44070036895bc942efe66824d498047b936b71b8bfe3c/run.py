from jinjamator.plugin_loader.content import contentPlugin
import inspect
import types
from pprint import pprint

class JinjamatorContentPluginDocumentor:

    def __init__(self):
        self._documentation = {'children': {}, 'full_path': ''}
        for (item_name, item) in globals().items():
            if isinstance(item, contentPlugin):
                self.traverse(item, item_name)

    def traverse(self, base, path):
        for item_name in dir(base):
            item = getattr(base, item_name)
            if isinstance(item, contentPlugin):
                self.traverse(item, path + '.' + item_name)
            if isinstance(item, types.FunctionType):
                if item_name.startswith('_'):
                    continue
                _cur = self._documentation
                for class_path in path.split('.'):
                    _prev = _cur
                    if not class_path in _cur['children']:
                        _cur['children'][class_path] = {}
                        _cur['children'][class_path]['children'] = {}
                        _cur['children'][class_path]['methods'] = {}
                        if _cur['full_path']:
                            _cur['children'][class_path]['full_path'] = _cur['full_path'] + '.' + class_path
                        else:
                            _cur['children'][class_path]['full_path'] = class_path
                    _cur = _cur['children'][class_path]
                _cur['methods'][item_name] = {'function_header': f'{path}.{item_name}{inspect.signature(item)}', 'doc': 'not documented yet', 'class_path': path}
                if item.__doc__:
                    _cur['methods'][item_name]['doc'] = item.__doc__.lstrip()
doc = JinjamatorContentPluginDocumentor()

def print_node(node_name, node):
    task.run('.generate_plugin_rst', {'node_name': node_name, 'node': node, 'textfile_output_path': f"{destination_directory}/{node['full_path']}.rst"}, output_plugin='textfile')

def generate(doc):
    for (node_name, node) in doc['children'].items():
        print_node(node_name, node)
        if node.get('children'):
            generate(node)
generate(doc._documentation)
task.run('.generate_toc_rst', {'file_list': list(doc._documentation['children'].keys()), 'textfile_output_path': f'{destination_directory}/index.rst'}, output_plugin='textfile')