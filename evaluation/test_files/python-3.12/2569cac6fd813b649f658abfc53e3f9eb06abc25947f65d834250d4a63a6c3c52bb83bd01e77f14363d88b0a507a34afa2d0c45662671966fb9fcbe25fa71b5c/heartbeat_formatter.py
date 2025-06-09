import time
from apscheduler.schedulers.background import BackgroundScheduler
from assemblyline.common import forge, metrics
from assemblyline.common.archiving import ARCHIVE_QUEUE_NAME
from assemblyline.common.constants import DISPATCH_TASK_HASH, SUBMISSION_QUEUE, SERVICE_STATE_HASH, ServiceStatus
from assemblyline.datastore.exceptions import SearchException
from assemblyline.odm.messages.scaler_heartbeat import ScalerMessage
from assemblyline.odm.messages.scaler_status_heartbeat import ScalerStatusMessage
from assemblyline.odm.messages.alerter_heartbeat import AlerterMessage
from assemblyline.odm.messages.archive_heartbeat import ArchiveMessage
from assemblyline.odm.messages.dispatcher_heartbeat import DispatcherMessage
from assemblyline.odm.messages.expiry_heartbeat import ExpiryMessage
from assemblyline.odm.messages.ingest_heartbeat import IngestMessage
from assemblyline.odm.messages.service_heartbeat import ServiceMessage
from assemblyline.remote.datatypes import get_client
from assemblyline.remote.datatypes.hash import Hash, ExpiringHash
from assemblyline.remote.datatypes.queues.comms import CommsQueue
from assemblyline.remote.datatypes.queues.named import NamedQueue
from assemblyline.remote.datatypes.queues.priority import PriorityQueue
from assemblyline_core.alerter.run_alerter import ALERT_QUEUE_NAME, ALERT_RETRY_QUEUE_NAME
from assemblyline_core.dispatching.dispatcher import Dispatcher
from assemblyline_core.ingester import INGEST_QUEUE_NAME, drop_chance
from assemblyline_core.ingester.constants import COMPLETE_QUEUE_NAME
STATUS_QUEUE = 'status'

def get_working_and_idle(redis, current_service):
    status_table = ExpiringHash(SERVICE_STATE_HASH, host=redis, ttl=30 * 60)
    service_data = status_table.items()
    busy = []
    idle = []
    for host, (service, state, time_limit) in service_data.items():
        if service == current_service:
            if time.time() < time_limit:
                if state == ServiceStatus.Running:
                    busy.append(host)
                else:
                    idle.append(host)
    return (busy, idle)

class HeartbeatFormatter(object):

    def __init__(self, sender, log, config=None, redis=None):
        self.sender = sender
        self.log = log
        self.config = config or forge.get_config()
        self.datastore = forge.get_datastore(self.config)
        self.redis = redis or get_client(host=self.config.core.redis.nonpersistent.host, port=self.config.core.redis.nonpersistent.port, private=False)
        self.redis_persist = get_client(host=self.config.core.redis.persistent.host, port=self.config.core.redis.persistent.port, private=False)
        self.status_queue = CommsQueue(STATUS_QUEUE, self.redis)
        self.dispatch_active_hash = Hash(DISPATCH_TASK_HASH, self.redis_persist)
        self.dispatcher_submission_queue = NamedQueue(SUBMISSION_QUEUE, self.redis)
        self.ingest_scanning = Hash('m-scanning-table', self.redis_persist)
        self.ingest_unique_queue = PriorityQueue('m-unique', self.redis_persist)
        self.ingest_queue = NamedQueue(INGEST_QUEUE_NAME, self.redis_persist)
        self.ingest_complete_queue = NamedQueue(COMPLETE_QUEUE_NAME, self.redis)
        self.alert_queue = NamedQueue(ALERT_QUEUE_NAME, self.redis_persist)
        self.alert_retry_queue = NamedQueue(ALERT_RETRY_QUEUE_NAME, self.redis_persist)
        self.archiver_queue = NamedQueue(ARCHIVE_QUEUE_NAME, self.redis_persist)
        constants = forge.get_constants(self.config)
        self.c_rng = constants.PRIORITY_RANGES['critical']
        self.h_rng = constants.PRIORITY_RANGES['high']
        self.m_rng = constants.PRIORITY_RANGES['medium']
        self.l_rng = constants.PRIORITY_RANGES['low']
        self.c_s_at = self.config.core.ingester.sampling_at['critical']
        self.h_s_at = self.config.core.ingester.sampling_at['high']
        self.m_s_at = self.config.core.ingester.sampling_at['medium']
        self.l_s_at = self.config.core.ingester.sampling_at['low']
        self.to_expire = {k: 0 for k in metrics.EXPIRY_METRICS}
        if self.config.core.expiry.batch_delete:
            self.delete_query = f'expiry_ts:[* TO {self.datastore.ds.now}-{self.config.core.expiry.delay}{self.datastore.ds.hour}/DAY]'
        else:
            self.delete_query = f'expiry_ts:[* TO {self.datastore.ds.now}-{self.config.core.expiry.delay}{self.datastore.ds.hour}]'
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.add_job(self._reload_expiry_queues, 'interval', seconds=self.config.core.metrics.export_interval * 4)
        self.scheduler.start()

    def _reload_expiry_queues(self):
        try:
            self.log.info('Refreshing expiry queues...')
            for collection_name in metrics.EXPIRY_METRICS:
                try:
                    collection = getattr(self.datastore, collection_name)
                    self.to_expire[collection_name] = collection.search(self.delete_query, rows=0, fl='id', track_total_hits='true')['total']
                except SearchException:
                    self.to_expire[collection_name] = 0
        except Exception:
            self.log.exception('Unknown exception occurred while reloading expiry queues:')

    def send_heartbeat(self, m_type, m_name, m_data, instances):
        if m_type == 'dispatcher':
            try:
                instances = sorted(Dispatcher.all_instances(self.redis_persist))
                inflight = {_i: Dispatcher.instance_assignment_size(self.redis_persist, _i) for _i in instances}
                queues = {_i: Dispatcher.all_queue_lengths(self.redis, _i) for _i in instances}
                msg = {'sender': self.sender, 'msg': {'inflight': {'max': self.config.core.dispatcher.max_inflight, 'outstanding': self.dispatch_active_hash.length(), 'per_instance': [inflight[_i] for _i in instances]}, 'instances': len(instances), 'metrics': m_data, 'queues': {'ingest': self.dispatcher_submission_queue.length(), 'start': [queues[_i]['start'] for _i in instances], 'result': [queues[_i]['result'] for _i in instances], 'command': [queues[_i]['command'] for _i in instances]}, 'component': m_name}}
                self.status_queue.publish(DispatcherMessage(msg).as_primitives())
                self.log.info(f"Sent dispatcher heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating DispatcherMessage')
        elif m_type == 'ingester':
            try:
                c_q_len = self.ingest_unique_queue.count(*self.c_rng)
                h_q_len = self.ingest_unique_queue.count(*self.h_rng)
                m_q_len = self.ingest_unique_queue.count(*self.m_rng)
                l_q_len = self.ingest_unique_queue.count(*self.l_rng)
                msg = {'sender': self.sender, 'msg': {'instances': instances, 'metrics': m_data, 'processing': {'inflight': self.ingest_scanning.length()}, 'processing_chance': {'critical': 1 - drop_chance(c_q_len, self.c_s_at), 'high': 1 - drop_chance(h_q_len, self.h_s_at), 'low': 1 - drop_chance(l_q_len, self.l_s_at), 'medium': 1 - drop_chance(m_q_len, self.m_s_at)}, 'queues': {'critical': c_q_len, 'high': h_q_len, 'ingest': self.ingest_queue.length(), 'complete': self.ingest_complete_queue.length(), 'low': l_q_len, 'medium': m_q_len}}}
                self.status_queue.publish(IngestMessage(msg).as_primitives())
                self.log.info(f"Sent ingester heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating IngestMessage')
        elif m_type == 'alerter':
            try:
                msg = {'sender': self.sender, 'msg': {'instances': instances, 'metrics': m_data, 'queues': {'alert': self.alert_queue.length(), 'alert_retry': self.alert_retry_queue.length()}}}
                self.status_queue.publish(AlerterMessage(msg).as_primitives())
                self.log.info(f"Sent alerter heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating AlerterMessage')
        elif m_type == 'expiry':
            try:
                msg = {'sender': self.sender, 'msg': {'instances': instances, 'metrics': m_data, 'queues': self.to_expire}}
                self.status_queue.publish(ExpiryMessage(msg).as_primitives())
                self.log.info(f"Sent expiry heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating ExpiryMessage')
        elif m_type == 'archiver':
            try:
                msg = {'sender': self.sender, 'msg': {'instances': instances, 'metrics': m_data, 'queued': self.archiver_queue.length()}}
                self.status_queue.publish(ArchiveMessage(msg).as_primitives())
                self.log.info(f"Sent archive heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating ArchiveMessage')
        elif m_type == 'scaler':
            try:
                msg = {'sender': self.sender, 'msg': {'instances': instances, 'metrics': m_data}}
                self.status_queue.publish(ScalerMessage(msg).as_primitives())
                self.log.info(f"Sent scaler heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating WatcherMessage')
        elif m_type == 'scaler_status':
            try:
                msg = {'sender': self.sender, 'msg': {'service_name': m_name, 'metrics': m_data}}
                self.status_queue.publish(ScalerStatusMessage(msg).as_primitives())
                self.log.info(f"Sent scaler status heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating WatcherMessage')
        elif m_type == 'service':
            try:
                busy, idle = get_working_and_idle(self.redis, m_name)
                msg = {'sender': self.sender, 'msg': {'instances': len(busy) + len(idle), 'metrics': m_data, 'activity': {'busy': len(busy), 'idle': len(idle)}, 'queue': forge.get_service_queue(m_name, self.redis).length(), 'service_name': m_name}}
                self.status_queue.publish(ServiceMessage(msg).as_primitives())
                self.log.info(f"Sent service heartbeat: {msg['msg']}")
            except Exception:
                self.log.exception('An exception occurred while generating ServiceMessage')
        else:
            self.log.warning(f'Skipping unknown counter: {m_name} [{m_type}] ==> {m_data}')