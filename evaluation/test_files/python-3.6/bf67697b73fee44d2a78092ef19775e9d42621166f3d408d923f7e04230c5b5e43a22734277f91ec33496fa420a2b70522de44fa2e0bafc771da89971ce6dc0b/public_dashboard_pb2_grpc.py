"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.cost_analysis.v1 import public_dashboard_pb2 as spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2

class PublicDashboardStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary('/spaceone.api.cost_analysis.v1.PublicDashboard/create', request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.CreatePublicDashboardRequest.SerializeToString, response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.FromString)
        self.update = channel.unary_unary('/spaceone.api.cost_analysis.v1.PublicDashboard/update', request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.UpdatePublicDashboardRequest.SerializeToString, response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.FromString)
        self.delete = channel.unary_unary('/spaceone.api.cost_analysis.v1.PublicDashboard/delete', request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.get = channel.unary_unary('/spaceone.api.cost_analysis.v1.PublicDashboard/get', request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.GetPublicDashboardRequest.SerializeToString, response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.FromString)
        self.list = channel.unary_unary('/spaceone.api.cost_analysis.v1.PublicDashboard/list', request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardQuery.SerializeToString, response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardsInfo.FromString)
        self.stat = channel.unary_unary('/spaceone.api.cost_analysis.v1.PublicDashboard/stat', request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardStatQuery.SerializeToString, response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString)

class PublicDashboardServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_PublicDashboardServicer_to_server(servicer, server):
    rpc_method_handlers = {'create': grpc.unary_unary_rpc_method_handler(servicer.create, request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.CreatePublicDashboardRequest.FromString, response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.SerializeToString), 'update': grpc.unary_unary_rpc_method_handler(servicer.update, request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.UpdatePublicDashboardRequest.FromString, response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.SerializeToString), 'delete': grpc.unary_unary_rpc_method_handler(servicer.delete, request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'get': grpc.unary_unary_rpc_method_handler(servicer.get, request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.GetPublicDashboardRequest.FromString, response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.SerializeToString), 'list': grpc.unary_unary_rpc_method_handler(servicer.list, request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardQuery.FromString, response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardsInfo.SerializeToString), 'stat': grpc.unary_unary_rpc_method_handler(servicer.stat, request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardStatQuery.FromString, response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('spaceone.api.cost_analysis.v1.PublicDashboard', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class PublicDashboard(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.PublicDashboard/create', spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.CreatePublicDashboardRequest.SerializeToString, spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.PublicDashboard/update', spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.UpdatePublicDashboardRequest.SerializeToString, spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.PublicDashboard/delete', spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.PublicDashboard/get', spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.GetPublicDashboardRequest.SerializeToString, spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.PublicDashboard/list', spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardQuery.SerializeToString, spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardsInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.PublicDashboard/stat', spaceone_dot_api_dot_cost__analysis_dot_v1_dot_public__dashboard__pb2.PublicDashboardStatQuery.SerializeToString, google_dot_protobuf_dot_struct__pb2.Struct.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)