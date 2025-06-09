import json
import traceback
from dust import logger
from dust.httpservices import SVCINFO_MODULE, DustResultType
from dust.httpservices.servicebase import ServiceBase
MODULE_ACTIONS = 'ACTIONS'
_services = []

class ActionController(ServiceBase):

    def __init__(self, *service_names):
        super().__init__(MODULE_ACTIONS)
        for service_name in service_names:
            _services.append(ServiceBase.get_service(service_name))

    def relay_action(self, params, request, response):
        ret = False
        name = params.get(SVCINFO_MODULE)
        services = None
        if name is None:
            services = _services
        else:
            services = []
            services.append(ServiceBase.get_service(name))
        for service in services:
            ret = ret or self.__relay_action(service, params, request, response)
        return ret

    def __relay_action(self, service, params, request, response):
        ret = False
        if service:
            try:
                result = service.do_process(params, request, response, immediate=True)
                if result.is_readon():
                    result = service.do_process(params, request, response, immediate=False)
                ret = result == DustResultType.ACCEPT
            except:
                traceback.print_exc()
                pass
            finally:
                pass
        return ret

    def do_process(self, params, request, response, immediate=True):
        ret = DustResultType.REJECT
        resp = {}
        for service in _services:
            if not service.do_process(params, request, resp, immediate).is_reject():
                service_name = service.get_modulename()
                ret = DustResultType.ACCEPT
                response[service_name] = resp
                resp = {}
        if ret != DustResultType.REJECT:
            self.log(response)
        return ret

    def log(self, action):
        logger().debug(json.dumps(action, indent=4))