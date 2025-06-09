import logging
logger = logging.getLogger(__name__)
from datetime import datetime
import os
import socket
from unicorncommon.server_status import SERVER_STATUS

class DBAgentException(Exception):

    def __init__(self, resp):
        self.resp = resp
        super().__init__()

    def __str__(self):
        return f"status: {self.resp['status']}"

class DBAgentClient:

    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger

    @property
    def my_logger(self):
        if self.logger is not None:
            return self.logger
        return logger

    def get_run(self, id):
        resp = self.client.send({'action': 'get-run', 'id': id})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp['payload']
        self.my_logger.error(f"get_run(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def get_application(self, id):
        resp = self.client.send({'action': 'get-application', 'id': id})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp['payload']
        self.my_logger.error(f"get_application(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def get_task(self, id):
        resp = self.client.send({'action': 'get-task', 'id': id})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp['payload']
        self.my_logger.error(f"get_task(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def set_run_started(self, id):
        start_time = datetime.utcnow().isoformat()
        resp = self.client.send({'action': 'set-run-started', 'id': id, 'start_time': start_time, 'pid': os.getpid()})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"set_run_started(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def set_run_finished(self, id, *, exit_code):
        finish_time = datetime.utcnow().isoformat()
        resp = self.client.send({'action': 'set-run-finished', 'id': id, 'finish_time': finish_time, 'exit_code': exit_code})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"set_run_finished(id={id}, exit_code={exit_code}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def unset_active_run(self, task_id):
        resp = self.client.send({'action': 'unset-active-run', 'task_id': task_id})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"unset_active_run(task_id={task_id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def set_active_run(self, task_id, *, run_id):
        resp = self.client.send({'action': 'set-active-run', 'task_id': task_id, 'run_id': run_id})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"set_active_run(task_id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def create_run(self, *, application_id, node_id, args, task_id=None):
        req = {'action': 'create-run', 'application_id': application_id, 'node_id': node_id, 'args': args}
        if task_id is not None:
            req['task_id'] = task_id
        resp = self.client.send(req)
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"create_run(application_id={application_id}, node_id={node_id}, args={args}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def delete_run(self, id):
        resp = self.client.send({'action': 'delete-run', 'id': id})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"delete_run(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def set_node_up(self, id, *, agent_classname, agent_endpoint, ip=None):
        up_time = datetime.utcnow().isoformat()
        hostname = socket.gethostname()
        if ip is None:
            ip = socket.gethostbyname(hostname)
        resp = self.client.send({'action': 'set-node-up', 'id': id, 'up_time': up_time, 'hostname': hostname, 'ip': ip, 'agent_classname': agent_classname, 'agent_endpoint': agent_endpoint})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"set_node_up(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)

    def set_node_down(self, id):
        down_time = datetime.utcnow().isoformat()
        resp = self.client.send({'action': 'set-node-down', 'id': id, 'down_time': down_time})
        if resp['status'] == SERVER_STATUS.OK.value:
            return resp.get('payload')
        self.my_logger.error(f"set_node_down(id={id}) failed, status = {resp['status']}")
        raise DBAgentException(resp=resp)