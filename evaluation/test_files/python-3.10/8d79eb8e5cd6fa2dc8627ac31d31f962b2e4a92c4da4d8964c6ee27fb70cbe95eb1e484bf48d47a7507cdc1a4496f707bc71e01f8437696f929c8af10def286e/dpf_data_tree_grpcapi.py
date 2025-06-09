import types
from ansys.dpf.gate.generated import dpf_data_tree_abstract_api
from ansys.dpf.gate import errors

def _get_stub(server):
    return server.get_stub(DpfDataTreeGRPCAPI.STUBNAME)

@errors.protect_grpc_class
class DpfDataTreeGRPCAPI(dpf_data_tree_abstract_api.DpfDataTreeAbstractAPI):
    STUBNAME = 'data_tree_stub'

    @staticmethod
    def init_dpf_data_tree_environment(object):
        from ansys.grpc.dpf import data_tree_pb2_grpc
        object._server.create_stub_if_necessary(DpfDataTreeGRPCAPI.STUBNAME, data_tree_pb2_grpc.DataTreeServiceStub)
        object._deleter_func = (_get_stub(object._server).Delete, lambda obj: obj._internal_obj if not isinstance(obj._internal_obj, (dict, list)) else None)

    @staticmethod
    def dpf_data_tree_new_on_client(client):
        from ansys.grpc.dpf import base_pb2
        return _get_stub(client).Create(base_pb2.Empty())

    @staticmethod
    def _dpf_data_tree_get_attribute(data_tree, attribute_name, value, type):
        if isinstance(data_tree._internal_obj, dict):
            value.set(data_tree._internal_obj[attribute_name])
            return
        from ansys.grpc.dpf import data_tree_pb2, base_pb2
        request = data_tree_pb2.GetRequest()
        request.data_tree.CopyFrom(data_tree._internal_obj)
        stype = base_pb2.Type.Value(type.upper())
        request.data.append(data_tree_pb2.SingleDataRequest(name=attribute_name, type=stype))
        data = _get_stub(data_tree._server).Get(request).data[0]
        if data.HasField('string'):
            value.set_str(data.string)
        elif data.HasField('int'):
            value.set(data.int)
        elif data.HasField('double'):
            value.set(data.double)
        elif data.HasField('vec_int'):
            value.set(data.vec_int.rep_int)
        elif data.HasField('vec_double'):
            value.set(data.vec_double.rep_double)
        elif data.HasField('vec_string'):
            value.set(data.vec_string.rep_string)
        elif data.HasField('data_tree'):
            return

    @staticmethod
    def dpf_data_tree_get_int_attribute(data_tree, attribute_name, value):
        DpfDataTreeGRPCAPI._dpf_data_tree_get_attribute(data_tree, attribute_name, value, 'int')

    @staticmethod
    def dpf_data_tree_get_double_attribute(data_tree, attribute_name, value):
        DpfDataTreeGRPCAPI._dpf_data_tree_get_attribute(data_tree, attribute_name, value, 'double')

    @staticmethod
    def dpf_data_tree_get_string_attribute(data_tree, attribute_name, data, size):
        DpfDataTreeGRPCAPI._dpf_data_tree_get_attribute(data_tree, attribute_name, data, 'string')

    @staticmethod
    def dpf_data_tree_get_vec_int_attribute(data_tree, attribute_name, data, size):
        DpfDataTreeGRPCAPI._dpf_data_tree_get_attribute(data_tree, attribute_name, data, 'vec_int')

    @staticmethod
    def dpf_data_tree_get_vec_double_attribute(data_tree, attribute_name, data, size):
        DpfDataTreeGRPCAPI._dpf_data_tree_get_attribute(data_tree, attribute_name, data, 'vec_double')

    @staticmethod
    def dpf_data_tree_get_string_collection_attribute(data_tree, attribute_name):
        from ansys.grpc.dpf import data_tree_pb2, base_pb2
        request = data_tree_pb2.GetRequest()
        request.data_tree.CopyFrom(data_tree._internal_obj)
        stype = base_pb2.Type.Value('VEC_STRING')
        request.data.append(data_tree_pb2.SingleDataRequest(name=attribute_name, type=stype))
        data = _get_stub(data_tree._server).Get(request).data[0]
        if data.HasField('vec_string'):
            return list(data.vec_string.rep_string)

    @staticmethod
    def dpf_data_tree_get_sub_tree(data_tree, sub_tree_name):
        from ansys.grpc.dpf import data_tree_pb2, base_pb2
        request = data_tree_pb2.GetRequest()
        request.data_tree.CopyFrom(data_tree._internal_obj)
        stype = base_pb2.Type.Value('DATA_TREE')
        request.data.append(data_tree_pb2.SingleDataRequest(name=sub_tree_name, type=stype))
        data = _get_stub(data_tree._server).Get(request).data[0]
        if data.HasField('data_tree'):
            return data.data_tree

    @staticmethod
    def _set_attribute_init(data_tree, attribute_name):
        if isinstance(data_tree._internal_obj, dict):
            request = types.SimpleNamespace(data_tree=data_tree._internal_obj, data=[])
            data = types.SimpleNamespace()
        else:
            from ansys.grpc.dpf import data_tree_pb2
            request = data_tree_pb2.UpdateRequest()
            request.data_tree.CopyFrom(data_tree._internal_obj)
            data = data_tree_pb2.Data()
        data.name = attribute_name
        request.data.append(data)
        return request

    @staticmethod
    def _set_attribute_finish(data_tree, request):
        if isinstance(data_tree._internal_obj, dict):
            if hasattr(request.data[0], 'int'):
                data_tree._internal_obj[request.data[0].name] = request.data[0].int
            elif hasattr(request.data[0], 'string'):
                data_tree._internal_obj[request.data[0].name] = request.data[0].string
        else:
            _get_stub(data_tree._server).Update(request)

    @staticmethod
    def dpf_data_tree_set_int_attribute(data_tree, attribute_name, value):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].int = value
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_set_vec_int_attribute(data_tree, attribute_name, value, size):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].vec_int.rep_int.extend(value)
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_set_double_attribute(data_tree, attribute_name, value):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].double = value
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_set_vec_double_attribute(data_tree, attribute_name, value, size):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].vec_double.rep_double.extend(value)
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_set_string_collection_attribute(data_tree, attribute_name, collection):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].vec_string.rep_string.extend(collection._internal_obj)
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_set_string_attribute(data_tree, attribute_name, data, size):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].string = data
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_set_sub_tree_attribute(data_tree, attribute_name, data):
        request = DpfDataTreeGRPCAPI._set_attribute_init(data_tree, attribute_name)
        request.data[0].data_tree.CopyFrom(data._internal_obj)
        DpfDataTreeGRPCAPI._set_attribute_finish(data_tree, request)

    @staticmethod
    def dpf_data_tree_has_attribute(data_tree, attribute_name):
        if isinstance(data_tree._internal_obj, dict):
            return attribute_name in data_tree._internal_obj
        from ansys.grpc.dpf import data_tree_pb2
        request = data_tree_pb2.HasRequest()
        request.data_tree.CopyFrom(data_tree._internal_obj)
        request.names.append(attribute_name)
        return _get_stub(data_tree._server).Has(request).has_each_name[attribute_name]