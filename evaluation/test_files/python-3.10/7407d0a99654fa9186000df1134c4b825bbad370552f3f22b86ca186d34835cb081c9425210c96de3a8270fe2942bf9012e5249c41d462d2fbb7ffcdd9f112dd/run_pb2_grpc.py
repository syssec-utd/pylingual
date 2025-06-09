"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ...thirdparty.kfpbackend import run_pb2 as thirdparty_dot_kfpbackend_dot_run__pb2

class RunServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/CreateRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.CreateRunRequest.SerializeToString, response_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.RunDetail.FromString)
        self.GetRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/GetRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.GetRunRequest.SerializeToString, response_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.RunDetail.FromString)
        self.ListRuns = channel.unary_unary('/thirdparty.kfpbackend.RunService/ListRuns', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ListRunsRequest.SerializeToString, response_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ListRunsResponse.FromString)
        self.ArchiveRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/ArchiveRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ArchiveRunRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.UnarchiveRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/UnarchiveRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.UnarchiveRunRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.DeleteRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/DeleteRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.DeleteRunRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.ReportRunMetrics = channel.unary_unary('/thirdparty.kfpbackend.RunService/ReportRunMetrics', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReportRunMetricsRequest.SerializeToString, response_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReportRunMetricsResponse.FromString)
        self.ReadArtifact = channel.unary_unary('/thirdparty.kfpbackend.RunService/ReadArtifact', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReadArtifactRequest.SerializeToString, response_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReadArtifactResponse.FromString)
        self.TerminateRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/TerminateRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.TerminateRunRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.RetryRun = channel.unary_unary('/thirdparty.kfpbackend.RunService/RetryRun', request_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.RetryRunRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class RunServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateRun(self, request, context):
        """Creates a new run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRun(self, request, context):
        """Finds a specific run by ID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListRuns(self, request, context):
        """Finds all runs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ArchiveRun(self, request, context):
        """Archives a run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnarchiveRun(self, request, context):
        """Restores an archived run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRun(self, request, context):
        """Deletes a run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReportRunMetrics(self, request, context):
        """ReportRunMetrics reports metrics of a run. Each metric is reported in its
        own transaction, so this API accepts partial failures. Metric can be
        uniquely identified by (run_id, node_id, name). Duplicate reporting will be
        ignored by the API. First reporting wins.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadArtifact(self, request, context):
        """Finds a run's artifact data.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TerminateRun(self, request, context):
        """Terminates an active run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetryRun(self, request, context):
        """Re-initiates a failed or terminated run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_RunServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreateRun': grpc.unary_unary_rpc_method_handler(servicer.CreateRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.CreateRunRequest.FromString, response_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.RunDetail.SerializeToString), 'GetRun': grpc.unary_unary_rpc_method_handler(servicer.GetRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.GetRunRequest.FromString, response_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.RunDetail.SerializeToString), 'ListRuns': grpc.unary_unary_rpc_method_handler(servicer.ListRuns, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ListRunsRequest.FromString, response_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ListRunsResponse.SerializeToString), 'ArchiveRun': grpc.unary_unary_rpc_method_handler(servicer.ArchiveRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ArchiveRunRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'UnarchiveRun': grpc.unary_unary_rpc_method_handler(servicer.UnarchiveRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.UnarchiveRunRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'DeleteRun': grpc.unary_unary_rpc_method_handler(servicer.DeleteRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.DeleteRunRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ReportRunMetrics': grpc.unary_unary_rpc_method_handler(servicer.ReportRunMetrics, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReportRunMetricsRequest.FromString, response_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReportRunMetricsResponse.SerializeToString), 'ReadArtifact': grpc.unary_unary_rpc_method_handler(servicer.ReadArtifact, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReadArtifactRequest.FromString, response_serializer=thirdparty_dot_kfpbackend_dot_run__pb2.ReadArtifactResponse.SerializeToString), 'TerminateRun': grpc.unary_unary_rpc_method_handler(servicer.TerminateRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.TerminateRunRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'RetryRun': grpc.unary_unary_rpc_method_handler(servicer.RetryRun, request_deserializer=thirdparty_dot_kfpbackend_dot_run__pb2.RetryRunRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('thirdparty.kfpbackend.RunService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class RunService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/CreateRun', thirdparty_dot_kfpbackend_dot_run__pb2.CreateRunRequest.SerializeToString, thirdparty_dot_kfpbackend_dot_run__pb2.RunDetail.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/GetRun', thirdparty_dot_kfpbackend_dot_run__pb2.GetRunRequest.SerializeToString, thirdparty_dot_kfpbackend_dot_run__pb2.RunDetail.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListRuns(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/ListRuns', thirdparty_dot_kfpbackend_dot_run__pb2.ListRunsRequest.SerializeToString, thirdparty_dot_kfpbackend_dot_run__pb2.ListRunsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ArchiveRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/ArchiveRun', thirdparty_dot_kfpbackend_dot_run__pb2.ArchiveRunRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnarchiveRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/UnarchiveRun', thirdparty_dot_kfpbackend_dot_run__pb2.UnarchiveRunRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/DeleteRun', thirdparty_dot_kfpbackend_dot_run__pb2.DeleteRunRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReportRunMetrics(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/ReportRunMetrics', thirdparty_dot_kfpbackend_dot_run__pb2.ReportRunMetricsRequest.SerializeToString, thirdparty_dot_kfpbackend_dot_run__pb2.ReportRunMetricsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadArtifact(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/ReadArtifact', thirdparty_dot_kfpbackend_dot_run__pb2.ReadArtifactRequest.SerializeToString, thirdparty_dot_kfpbackend_dot_run__pb2.ReadArtifactResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TerminateRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/TerminateRun', thirdparty_dot_kfpbackend_dot_run__pb2.TerminateRunRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetryRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/thirdparty.kfpbackend.RunService/RetryRun', thirdparty_dot_kfpbackend_dot_run__pb2.RetryRunRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)