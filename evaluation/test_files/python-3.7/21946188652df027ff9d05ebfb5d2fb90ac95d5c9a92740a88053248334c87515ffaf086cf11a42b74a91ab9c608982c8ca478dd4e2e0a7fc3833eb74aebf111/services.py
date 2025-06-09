from django_grpc_framework import generics
from temba.flows.models import Flow
from weni.grpc.flow.serializers import FlowProtoSerializer
from weni.grpc.core.services import AbstractService

class FlowService(generics.GenericService, AbstractService):

    def List(self, request, _):
        org = self.get_org_object(request.org_uuid, 'uuid')
        queryset = Flow.objects.filter(name__icontains=request.flow_name, org=org.id, is_active=True).exclude(is_archived=True)[:20]
        serializer = FlowProtoSerializer(queryset, many=True)
        for message in serializer.message:
            yield message