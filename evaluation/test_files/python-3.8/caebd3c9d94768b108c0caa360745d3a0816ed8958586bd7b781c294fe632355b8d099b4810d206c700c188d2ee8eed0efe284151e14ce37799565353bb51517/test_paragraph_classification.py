import asyncio
from typing import AsyncIterator
import aiohttp
import pytest
from nucliadb_protos.dataset_pb2 import ParagraphClassificationBatch, TaskType, TrainSet
from nucliadb_protos.knowledgebox_pb2 import Label, LabelSet
from nucliadb_protos.resources_pb2 import Metadata, ParagraphAnnotation, UserFieldMetadata
from nucliadb_protos.writer_pb2 import BrokerMessage, SetLabelsRequest
from nucliadb_protos.writer_pb2_grpc import WriterStub
from nucliadb.tests.utils import inject_message
from nucliadb.train import API_PREFIX
from nucliadb.train.api.v1.router import KB_PREFIX

async def get_paragraph_classification_batch_from_response(response: aiohttp.ClientResponse) -> AsyncIterator[ParagraphClassificationBatch]:
    while True:
        header = await response.content.read(4)
        if header == b'':
            break
        payload_size = int.from_bytes(header, byteorder='big', signed=False)
        payload = await response.content.read(payload_size)
        pcb = ParagraphClassificationBatch()
        pcb.ParseFromString(payload)
        assert pcb.data
        yield pcb

def broker_resource(knowledgebox: str) -> BrokerMessage:
    import uuid
    from datetime import datetime
    from nucliadb_protos import resources_pb2 as rpb
    rid = str(uuid.uuid4())
    slug = f'{rid}slug1'
    bm: BrokerMessage = BrokerMessage(kbid=knowledgebox, uuid=rid, slug=slug, type=BrokerMessage.AUTOCOMMIT)
    bm.basic.icon = 'text/plain'
    bm.basic.title = 'Title Resource'
    bm.basic.summary = 'Summary of document'
    bm.basic.thumbnail = 'doc'
    bm.basic.layout = 'default'
    bm.basic.metadata.useful = True
    bm.basic.metadata.status = Metadata.Status.PROCESSED
    bm.basic.metadata.language = 'es'
    bm.basic.created.FromDatetime(datetime.now())
    bm.basic.modified.FromDatetime(datetime.now())
    bm.origin.source = rpb.Origin.Source.WEB
    c4 = rpb.Classification()
    c4.label = 'label_user'
    c4.labelset = 'labelset_resources'
    bm.basic.usermetadata.classifications.append(c4)
    etw = rpb.ExtractedTextWrapper()
    etw.body.text = 'My own text Ramon. This is great to be here. \n Where is my beer? Do you want to go shooping? This is a test!'
    etw.field.field = 'file'
    etw.field.field_type = rpb.FieldType.FILE
    bm.extracted_text.append(etw)
    c3 = rpb.Classification()
    c3.label = 'label_user'
    c3.labelset = 'labelset_paragraphs'
    pa = ParagraphAnnotation()
    pa.classifications.append(c3)
    pa.key = 'N_RID/f/file/47-64'
    ufm = UserFieldMetadata()
    ufm.paragraphs.append(pa)
    pa = ParagraphAnnotation()
    pa.classifications.append(c3)
    pa.key = 'N_RID/f/file/0-45'
    ufm.paragraphs.append(pa)
    pa = ParagraphAnnotation()
    pa.classifications.append(c3)
    pa.key = 'N_RID/f/file/65-93'
    ufm.paragraphs.append(pa)
    pa = ParagraphAnnotation()
    pa.classifications.append(c3)
    pa.key = 'N_RID/f/file/93-109'
    ufm.paragraphs.append(pa)
    ufm.field.field = 'file'
    ufm.field.field_type = rpb.FieldType.FILE
    bm.basic.fieldmetadata.append(ufm)
    etw = rpb.ExtractedTextWrapper()
    etw.body.text = 'Summary of document'
    etw.field.field = 'summary'
    etw.field.field_type = rpb.FieldType.GENERIC
    bm.extracted_text.append(etw)
    etw = rpb.ExtractedTextWrapper()
    etw.body.text = 'Title Resource'
    etw.field.field = 'title'
    etw.field.field_type = rpb.FieldType.GENERIC
    bm.extracted_text.append(etw)
    bm.files['file'].added.FromDatetime(datetime.now())
    bm.files['file'].file.source = rpb.CloudFile.Source.EXTERNAL
    c1 = rpb.Classification()
    c1.label = 'label_machine'
    c1.labelset = 'labelset_paragraphs'
    c2 = rpb.Classification()
    c2.label = 'label_machine'
    c2.labelset = 'labelset_resources'
    fcm = rpb.FieldComputedMetadataWrapper()
    fcm.field.field = 'file'
    fcm.field.field_type = rpb.FieldType.FILE
    p1 = rpb.Paragraph(start=0, end=45)
    p1.classifications.append(c1)
    p2 = rpb.Paragraph(start=47, end=64)
    p2.classifications.append(c1)
    p3 = rpb.Paragraph(start=65, end=93)
    p3.classifications.append(c1)
    p4 = rpb.Paragraph(start=93, end=109)
    p4.classifications.append(c1)
    fcm.metadata.metadata.paragraphs.append(p1)
    fcm.metadata.metadata.paragraphs.append(p2)
    fcm.metadata.metadata.paragraphs.append(p3)
    fcm.metadata.metadata.paragraphs.append(p4)
    fcm.metadata.metadata.last_index.FromDatetime(datetime.now())
    fcm.metadata.metadata.last_understanding.FromDatetime(datetime.now())
    fcm.metadata.metadata.last_extract.FromDatetime(datetime.now())
    fcm.metadata.metadata.ner['Ramon'] = 'PERSON'
    fcm.metadata.metadata.classifications.append(c2)
    bm.field_metadata.append(fcm)
    ev = rpb.ExtractedVectorsWrapper()
    ev.field.field = 'file'
    ev.field.field_type = rpb.FieldType.FILE
    bm.source = BrokerMessage.MessageSource.WRITER
    return bm

async def inject_resource_with_paragraph_labels(knowledgebox, writer):
    bm = broker_resource(knowledgebox)
    await inject_message(writer, bm)
    return bm.uuid

@pytest.mark.asyncio
async def test_generator_paragraph_classification(train_rest_api: aiohttp.ClientSession, knowledgebox: str, nucliadb_grpc: WriterStub):
    slr = SetLabelsRequest()
    slr.kb.uuid = knowledgebox
    slr.id = 'labelset_paragraphs'
    slr.labelset.kind.append(LabelSet.LabelSetKind.PARAGRAPHS)
    l1 = Label(title='label_machine')
    l2 = Label(title='label_user')
    slr.labelset.labels.append(l1)
    slr.labelset.labels.append(l2)
    await nucliadb_grpc.SetLabels(slr)
    slr = SetLabelsRequest()
    slr.kb.uuid = knowledgebox
    slr.id = 'labelset_resources'
    slr.labelset.kind.append(LabelSet.LabelSetKind.RESOURCES)
    l1 = Label(title='label_machine')
    l2 = Label(title='label_user')
    slr.labelset.labels.append(l1)
    slr.labelset.labels.append(l2)
    await nucliadb_grpc.SetLabels(slr)
    await inject_resource_with_paragraph_labels(knowledgebox, nucliadb_grpc)
    await asyncio.sleep(0.1)
    async with train_rest_api.get(f'/{API_PREFIX}/v1/{KB_PREFIX}/{knowledgebox}/trainset') as partitions:
        assert partitions.status == 200
        data = await partitions.json()
        assert len(data['partitions']) == 1
        partition_id = data['partitions'][0]
    trainset = TrainSet()
    trainset.type = TaskType.PARAGRAPH_CLASSIFICATION
    trainset.batch_size = 2
    trainset.filter.labels.append('labelset_paragraphs')
    async with train_rest_api.post(f'/{API_PREFIX}/v1/{KB_PREFIX}/{knowledgebox}/trainset/{partition_id}', data=trainset.SerializeToString()) as response:
        assert response.status == 200
        batches = []
        async for batch in get_paragraph_classification_batch_from_response(response):
            batches.append(batch)
            assert len(batch.data) == 2
        assert len(batches) == 2