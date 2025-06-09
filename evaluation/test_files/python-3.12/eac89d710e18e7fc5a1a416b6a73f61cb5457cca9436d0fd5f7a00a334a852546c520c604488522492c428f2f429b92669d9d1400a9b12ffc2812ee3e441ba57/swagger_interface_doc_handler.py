import inspect
from lesscode.utils.doc.interface_doc_handler import swagger_json_project, swagger_json_class, python_column_type_dict
from lesscode.web.base_handler import BaseHandler
from lesscode.web.router_mapping import Handler, GetMapping
from tornado.options import options

@Handler('/swagger_interface', desc='swagger接口')
class SwaggerInterfaceDocHandler(BaseHandler):

    @GetMapping(title='获取swagger接口文档')
    def get_swagger_data_doc(self):
        paths = {}
        for class_json in swagger_json_project:
            for method in class_json['method_list']:
                paths[options.route_prefix + class_json['route'] + method['route']] = {method['http_method']: {'tags': [class_json['desc']], 'description': method['description'], 'parameters': method['parameters'], 'responses': {'200': {'description': 'successful operation'}}}}
        result = {'swagger': '2.0', 'info': {'title': '{}API'.format(options.application_name), 'version': '0.1.0'}, 'definitions': {}, 'servers': [{'url': 'http://{}:{}/'.format(options.outside_screen_ip, options.port), 'description': ''}], 'host': '{}:{}/'.format(options.outside_screen_ip, options.port), 'paths': paths}
        self.original = True
        self.write(result)