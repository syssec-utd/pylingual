from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from papermerge.core.models import Document
from papermerge.core.tasks import ocr_document_task, post_ocr_document_task
from papermerge.core.storage import default_storage
from papermerge.core.serializers import OcrSerializer
from .mixins import RequireAuthMixin

class OCRView(RequireAuthMixin, GenericAPIView):
    serializer_class = OcrSerializer

    def post(self, request):
        """
        Starts OCR for document version
        """
        doc_id = request.data['doc_id']
        lang = request.data['lang']
        doc = get_object_or_404(Document.objects, pk=doc_id)
        namespace = getattr(default_storage, 'namespace', None)
        ocr_document_task.apply_async(kwargs={'document_id': str(doc.id), 'lang': lang, 'namespace': namespace, 'user_id': str(request.user.id)}, link=post_ocr_document_task.s(namespace))
        return Response({'message': 'OCR successfully started'})