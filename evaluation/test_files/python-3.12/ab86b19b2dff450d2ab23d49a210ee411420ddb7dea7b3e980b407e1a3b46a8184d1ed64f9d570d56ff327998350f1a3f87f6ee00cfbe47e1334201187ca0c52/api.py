from .dataset import AdxDataset
from .writer_fs import AdxDatasetWriterFs
from .writer_s3 import AdxDatasetWriterS3

def get_adx_dataset_revisions(dataset_id, /, *, start_date=None, end_date=None):
    client = AdxDataset(dataset_id=dataset_id, writer=None)
    return client.get_revisions(start_date, end_date)

def download_adx_dataset_revision(root_path, dataset_id, revision_id=None, /, *, prefix=None):
    writer = AdxDatasetWriterFs(root_path=root_path, prefix=prefix)
    client = AdxDataset(dataset_id=dataset_id, writer=writer)
    if revision_id is None:
        rev = client.get_latest_revision()
        if rev is None:
            raise RuntimeError('No revisions in dataset')
        revision_id = rev['Id']
    client.export_revision(revision_id)

def export_single_adx_dataset_revision_to_s3(bucket, dataset_id, revision_id=None, /, *, prefix=None):
    writer = AdxDatasetWriterS3(bucket=bucket, prefix=prefix)
    client = AdxDataset(dataset_id=dataset_id, writer=writer)
    if revision_id is None:
        rev = client.get_latest_revision()
        if rev is None:
            raise RuntimeError('No revisions in dataset')
        revision_id = rev['Id']
    client.export_revision(revision_id)

def export_multiple_adx_dataset_revisions_to_s3(bucket, dataset_id, /, *, prefix=None, start_date=None, end_date=None):
    writer = AdxDatasetWriterS3(bucket=bucket, prefix=prefix)
    client = AdxDataset(dataset_id=dataset_id, writer=writer)
    client.export_revisions(start_date, end_date)

def enable_auto_exporting_adx_dataset_revisions_to_s3(bucket, dataset_id, /, *, prefix=None):
    writer = AdxDatasetWriterS3(bucket=bucket, prefix=prefix)
    client = AdxDataset(dataset_id=dataset_id, writer=writer)
    client.auto_export_revisions()

def disable_auto_exporting_adx_dataset_revisions_to_s3(dataset_id):
    client = AdxDataset(dataset_id=dataset_id, writer=None)
    client.delete_all_auto_revision_exports()