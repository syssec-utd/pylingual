from typing import Dict
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from pyramid.httpexceptions import HTTPOk
from pyramid.request import Request
from pyramid.view import view_config
from ... import security, resource
from ...models import MetaDatum, MetaDataSet, MetaDatumRecord, File
from ..metadatasets import MetaDataSetResponse
from ...utils import get_record_from_metadataset
from ..metadata import get_all_metadata
from ..files import FileResponse

def get_pending_metadatasets(dbsession, user, metadata: Dict[str, MetaDatum]):
    m_sets = dbsession.query(MetaDataSet).filter(and_(MetaDataSet.user == user, MetaDataSet.submission_id.is_(None))).options(joinedload(MetaDataSet.metadatumrecords).joinedload(MetaDatumRecord.metadatum)).all()
    return [MetaDataSetResponse(id=resource.get_identifier(m_set), record=get_record_from_metadataset(m_set, metadata), file_ids={name: None for name, metadatum in metadata.items() if metadatum.isfile}, user_id=resource.get_identifier(m_set.user), submission_id=resource.get_identifier(m_set.submission) if m_set.submission else None) for m_set in m_sets]

def get_pending_files(dbsession, user):
    db_files = dbsession.query(File).outerjoin(MetaDatumRecord).filter(and_(File.user_id == user.id, MetaDatumRecord.id.is_(None), File.content_uploaded.is_(True))).order_by(File.id.desc())
    return [FileResponse(id=resource.get_identifier(db_file), name=db_file.name, content_uploaded=db_file.content_uploaded, checksum=db_file.checksum, filesize=db_file.filesize, user_id=resource.get_identifier(db_file.user), expires=db_file.upload_expires.isoformat() if db_file.upload_expires else None) for db_file in db_files]

@view_config(route_name='pending', renderer='json', request_method='GET')
def get(request: Request) -> HTTPOk:
    """Get all pending medatasets and files with validation information

    Raises:
        401 HTTPUnauthorized - Authorization not available
    """
    db = request.dbsession
    auth_user = security.revalidate_user(request)
    metadata = get_all_metadata(db, include_service_metadata=False)
    mdat_names = list(metadata.keys())
    mdat_names_files = [mdat_name for mdat_name, mdat in metadata.items() if mdat.isfile]
    return {'metadataKeys': mdat_names, 'metadataKeysFiles': mdat_names_files, 'metadatasets': get_pending_metadatasets(db, auth_user, metadata), 'files': get_pending_files(db, auth_user)}