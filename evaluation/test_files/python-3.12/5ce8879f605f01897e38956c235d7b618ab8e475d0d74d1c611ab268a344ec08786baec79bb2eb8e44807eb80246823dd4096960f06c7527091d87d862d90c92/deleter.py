import logging
from odoo import _
from odoo.addons.component.core import Component
from odoo.addons.queue_job.exception import RetryableJobError
from ...fields import MilliDatetime
_logger = logging.getLogger(__name__)

class AnalyticLineBatchDeleter(Component):
    """Batch Deleter working with a jira.backend.timestamp.record

    It locks the timestamp to ensure no other job is working on it,
    and uses the latest timestamp value as reference for the search.

    The role of a BatchDeleter is to search for a list of
    items to delete and schedule jobs for the deletions.
    """
    _name = 'jira.analytic.line.timestamp.batch.deleter'
    _inherit = ['base.synchronizer', 'jira.base']
    _usage = 'timestamp.batch.deleter'

    def run(self, timestamp, **kwargs):
        """Run the synchronization using the timestamp"""
        original_timestamp_value = timestamp.last_timestamp
        if not timestamp._lock():
            self._handle_lock_failed(timestamp)
        next_timestamp_value, records = self._search(timestamp)
        timestamp._update_timestamp(next_timestamp_value)
        number = self._handle_records(records)
        return _('Batch from {} UTC to {} UTC generated {} delete jobs').format(original_timestamp_value, next_timestamp_value, number)

    def _handle_records(self, records):
        """Handle the records to import and return the number handled"""
        for record_id in records:
            self._delete_record(record_id)
        return len(records)

    def _handle_lock_failed(self, timestamp):
        _logger.warning('Failed to acquire timestamps %s', timestamp, exc_info=True)
        raise RetryableJobError('Concurrent job / process already syncing', ignore_retry=True)

    def _search(self, timestamp):
        unix_timestamp = MilliDatetime.to_timestamp(timestamp.last_timestamp)
        result = self.backend_adapter.deleted_since(since=unix_timestamp)
        worklog_ids = result.deleted_worklog_ids
        next_timestamp = MilliDatetime.from_timestamp(result.until)
        return (next_timestamp, worklog_ids)

    def _delete_record(self, record_id, **kwargs):
        """Delay the delete of the records"""
        self.model.with_delay(description=_('Delete a local worklog which has been deleted on JIRA'), **kwargs).delete_record(self.backend_record, record_id, only_binding=False, set_inactive=False)