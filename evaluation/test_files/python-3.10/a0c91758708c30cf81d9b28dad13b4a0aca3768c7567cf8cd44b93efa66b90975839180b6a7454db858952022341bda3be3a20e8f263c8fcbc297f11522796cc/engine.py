"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging
import random
import time
from functools import wraps
from typing import Optional
from . import states, validator
from .eri import DataInput, EngineRuntimeInterface, ExecutionData, Node, NodeType, ScheduleType, State
from .exceptions import InvalidOperationError, NotFoundError
from .handler import HandlerFactory
from .interrupt import ExecuteInterrupter, ExecuteKeyPoint, InterruptException, ScheduleInterrupter, ScheduleKeyPoint
from .local import CurrentNodeInfo, clear_node_info, set_node_info
from .metrics import ENGINE_NODE_EXECUTE_TIME, ENGINE_NODE_SCHEDULE_TIME, ENGINE_PROCESS_RUNNING_TIME, ENGINE_RUNNING_PROCESSES, ENGINE_RUNNING_SCHEDULES, ENGINE_SCHEDULE_RUNNING_TIME, ENGINE_EXECUTE_PRE_PROCESS_DURATION, ENGINE_EXECUTE_POST_PROCESS_DURATION, ENGINE_SCHEDULE_PRE_PROCESS_DURATION, ENGINE_SCHEDULE_POST_PROCESS_DURATION, setup_gauge, setup_histogram
from .utils.host import get_hostname
from .utils.string import get_lower_case_name
logger = logging.getLogger('bamboo_engine')

def interrupt_exception_catcher(func):

    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InterruptException:
            pass
        finally:
            clear_node_info()
    return _wrapper

class Engine:
    """
    流程引擎，封装流程核心调度逻辑
    """
    PURE_SKIP_ENABLE_NODE_TYPE = {NodeType.ServiceActivity, NodeType.EmptyStartEvent}

    def __init__(self, runtime: EngineRuntimeInterface):
        self.runtime = runtime
        self._hostname = get_hostname()

    def run_pipeline(self, pipeline: dict, root_pipeline_data: Optional[dict]=None, root_pipeline_context: Optional[dict]=None, subprocess_context: Optional[dict]=None, **options):
        """
        运行流程

        :param pipeline: 流程数据
        :type pipeline: dict
        :param root_pipeline_data 根流程数据
        :type root_pipeline_data: dict
        :param root_pipeline_context 根流程上下文
        :type root_pipeline_context: dict
        :param subprocess_context 子流程预置流程上下文
        :type subprocess_context: dict
        """
        root_pipeline_data = {} if root_pipeline_data is None else root_pipeline_data
        root_pipeline_context = {} if root_pipeline_context is None else root_pipeline_context
        subprocess_context = {} if subprocess_context is None else subprocess_context
        cycle_tolerate = options.get('cycle_tolerate', False)
        validator.validate_and_process_pipeline(pipeline, cycle_tolerate)
        self.runtime.pre_prepare_run_pipeline(pipeline, root_pipeline_data, root_pipeline_context, subprocess_context, **options)
        process_id = self.runtime.prepare_run_pipeline(pipeline, root_pipeline_data, root_pipeline_context, subprocess_context, **options)
        self.runtime.execute(process_id=process_id, node_id=pipeline['start_event']['id'], root_pipeline_id=pipeline['id'], parent_pipeline_id=pipeline['id'])
        self.runtime.post_prepare_run_pipeline(pipeline, root_pipeline_data, root_pipeline_context, subprocess_context, **options)

    def pause_pipeline(self, pipeline_id: str):
        """
        暂停流程

        :param pipeline_id: 流程 ID
        :type pipeline_id: str
        """
        if not self.runtime.has_state(pipeline_id):
            raise NotFoundError('node({}) does not exist'.format(pipeline_id))
        self.runtime.pre_pause_pipeline(pipeline_id)
        self.runtime.set_state(node_id=pipeline_id, to_state=states.SUSPENDED)
        self.runtime.post_pause_pipeline(pipeline_id)

    def revoke_pipeline(self, pipeline_id: str):
        """
        撤销流程

        :param pipeline_id: 流程 ID
        :type pipeline_id: str
        """
        if not self.runtime.has_state(pipeline_id):
            raise NotFoundError('node({}) does not exist'.format(pipeline_id))
        self.runtime.pre_revoke_pipeline(pipeline_id)
        self.runtime.set_state(node_id=pipeline_id, to_state=states.REVOKED)
        self.runtime.post_revoke_pipeline(pipeline_id)

    def resume_pipeline(self, pipeline_id: str):
        """
        继续流程

        :param pipeline_id: 流程 ID
        :type pipeline_id: str
        """
        state = self.runtime.get_state(pipeline_id)
        if state.name != states.SUSPENDED:
            raise InvalidOperationError('pipeline({}) state is: {}'.format(pipeline_id, state.name))
        info_list = self.runtime.get_suspended_process_info(pipeline_id)
        self.runtime.pre_resume_pipeline(pipeline_id)
        self.runtime.set_state(node_id=pipeline_id, to_state=states.RUNNING)
        if info_list:
            self.runtime.batch_resume(process_id_list=[i.process_id for i in info_list])
            for info in info_list:
                self.runtime.execute(process_id=info.process_id, node_id=info.current_node, root_pipeline_id=info.root_pipeline_id, parent_pipeline_id=info.top_pipeline_id)
        self.runtime.post_resume_pipeline(pipeline_id)

    def pause_node_appoint(self, node_id: str):
        """
        预约暂停节点

        :param node_id: 节点 ID
        :type node_id: str
        """
        node = self.runtime.get_node(node_id)
        if node.type == NodeType.SubProcess:
            raise InvalidOperationError('can not use pause_node_appoint api for {}'.format(node.type))
        self.runtime.pre_pause_node(node_id)
        self.runtime.set_state(node_id=node_id, to_state=states.SUSPENDED)
        self.runtime.post_pause_node(node_id)

    def resume_node_appoint(self, node_id: str):
        """
        继续由于节点暂停被阻塞的流程的执行

        :param node_id: 节点 ID
        :type node_id: str
        """
        node = self.runtime.get_node(node_id)
        if node.type == NodeType.SubProcess:
            raise InvalidOperationError('can not use pause_node_appoint api for {}'.format(node.type))
        self.runtime.pre_resume_node(node_id)
        info_list = self.runtime.get_suspended_process_info(node_id)
        self.runtime.set_state(node_id=node_id, to_state=states.READY)
        for info in info_list:
            self.runtime.resume(process_id=info.process_id)
            self.runtime.execute(process_id=info.process_id, node_id=info.current_node, root_pipeline_id=info.root_pipeline_id, parent_pipeline_id=info.top_pipeline_id)
        self.runtime.post_resume_node(node_id)

    def retry_node(self, node_id: str, data: Optional[dict]=None):
        """
        重试节点

        :param node_id: 节点 ID
        :type node_id: str
        :param data: 重试时使用的输入数据, defaults to None
        :type data: Optional[dict], optional
        """
        node = self.runtime.get_node(node_id)
        escape_render_keys = data.pop('_escape_render_keys', []) if data else []
        if not node.can_retry:
            raise InvalidOperationError('can not retry node({}) with can_retry({})'.format(node_id, node.can_retry))
        state = self.runtime.get_state(node_id)
        process_info = self._ensure_state_is_fail_and_return_process_info(state)
        self.runtime.pre_retry_node(node_id, data)
        if data is not None:
            self.runtime.set_data_inputs(node_id, {k: DataInput(need_render=False if k in escape_render_keys else True, value=v) for (k, v) in data.items()})
        self._add_history(node_id, state)
        self.runtime.set_state(node_id=node_id, to_state=states.READY, is_retry=True, refresh_version=True, clear_started_time=True, clear_archived_time=True)
        self.runtime.execute(process_id=process_info.process_id, node_id=node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id)
        self.runtime.post_retry_node(node_id, data)

    def retry_subprocess(self, node_id: str):
        """
        重试进入失败的子流程

        :param node_id: 子流程 ID
        :type node_id: str
        :raises InvalidOperationError: [description]
        """
        node = self.runtime.get_node(node_id)
        if node.type is not NodeType.SubProcess:
            raise InvalidOperationError('node({}) type is not SubProcess'.format(node_id))
        state = self.runtime.get_state(node_id)
        process_info = self._ensure_state_is_fail_and_return_process_info(state)
        self.runtime.pre_retry_subprocess(node_id)
        if process_info.pipeline_stack[-1] == node_id:
            self.runtime.set_pipeline_stack(process_info.process_id, process_info.pipeline_stack[:-1])
        self._add_history(node_id, state)
        self.runtime.set_state(node_id=node_id, to_state=states.READY, is_retry=True, refresh_version=True, clear_started_time=True, clear_archived_time=True)
        self.runtime.execute(process_id=process_info.process_id, node_id=node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id)
        self.runtime.post_retry_subprocess(node_id)

    def skip_node(self, node_id: str):
        """
        跳过失败的节点继续执行

        :param node_id: 节点 ID
        :type node_id: str
        :raises InvalidOperationError: [description]
        :raises InvalidOperationError: [description]
        """
        node = self.runtime.get_node(node_id)
        if not node.can_skip:
            raise InvalidOperationError('can not skip this node')
        if node.type not in self.PURE_SKIP_ENABLE_NODE_TYPE:
            raise InvalidOperationError('can not use skip_node api for {}'.format(node.type))
        state = self.runtime.get_state(node_id)
        process_info = self._ensure_state_is_fail_and_return_process_info(state)
        self.runtime.pre_skip_node(node_id)
        next_node_id = node.target_nodes[0]
        self._add_history(node_id, state)
        self.runtime.set_state(node_id=node_id, to_state=states.FINISHED, is_skip=True, refresh_version=True, set_archive_time=True)
        self.runtime.execute(process_id=process_info.process_id, node_id=next_node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id)
        self.runtime.post_skip_node(node_id)

    def skip_exclusive_gateway(self, node_id: str, flow_id: str):
        """
        跳过执行失败的分支网关继续执行

        :param node_id: 节点 ID
        :type node_id: str
        :param flow_id: 需要继续执行的流 ID
        :type flow_id: str
        :raises InvalidOperationError: [description]
        """
        node = self.runtime.get_node(node_id)
        if node.type != NodeType.ExclusiveGateway:
            raise InvalidOperationError('{} is not exclusive gateway, actual: {}'.format(node_id, node.type.value))
        next_node_id = node.targets[flow_id]
        state = self.runtime.get_state(node_id)
        process_info = self._ensure_state_is_fail_and_return_process_info(state)
        self.runtime.pre_skip_exclusive_gateway(node_id, flow_id)
        self._add_history(node_id, state)
        self.runtime.set_state(node_id=node_id, to_state=states.FINISHED, is_skip=True, refresh_version=True, set_archive_time=True)
        self.runtime.execute(process_id=process_info.process_id, node_id=next_node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id)
        self.runtime.post_skip_exclusive_gateway(node_id, flow_id)

    def skip_conditional_parallel_gateway(self, node_id: str, flow_ids: list, converge_gateway_id: str):
        """
        跳过执行失败的条件并行网关继续执行

        :param node_id: 节点 ID
        :type node_id: str
        :param flow_ids: 需要继续执行的流 ID 列表
        :type flow_ids: list
        :param converge_gateway_id: 目标汇聚网关 ID
        :type converge_gateway_id: str
        :raises InvalidOperationError: [description]
        """
        node = self.runtime.get_node(node_id)
        if node.type != NodeType.ConditionalParallelGateway:
            raise InvalidOperationError('{} is not conditional parallel gateway, actual: {}'.format(node_id, node.type.value))
        state = self.runtime.get_state(node_id)
        process_info = self._ensure_state_is_fail_and_return_process_info(state)
        process_id = process_info.process_id
        self.runtime.pre_skip_conditional_parallel_gateway(node_id, flow_ids, converge_gateway_id)
        self.runtime.sleep(process_id)
        fork_targets = [node.targets[flow_id] for flow_id in flow_ids]
        from_to = {target: converge_gateway_id for target in fork_targets}
        dispatch_processes = self.runtime.fork(parent_id=process_info.process_id, root_pipeline_id=process_info.root_pipeline_id, pipeline_stack=process_info.pipeline_stack, from_to=from_to)
        children = [d.process_id for d in dispatch_processes]
        self.runtime.join(process_id, children)
        for d in dispatch_processes:
            self.runtime.execute(process_id=d.process_id, node_id=d.node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id)
        self._add_history(node_id, state)
        self.runtime.set_state(node_id=node_id, to_state=states.FINISHED, is_skip=True, refresh_version=True, set_archive_time=True)
        self.runtime.post_skip_conditional_parallel_gateway(node_id, flow_ids, converge_gateway_id)

    def forced_fail_activity(self, node_id: str, ex_data: str, send_post_set_state_signal: bool=True):
        """
        强制失败某个 Activity

        :param node_id: 节点 ID
        :type node_id: str
        :param ex_data: 强制失败时写入节点有慈航数据的信息
        :type ex_data: str
        :param send_post_set_state_signal: 强制失败时，是否发送post_set_state信号
        :type send_post_set_state_signal: bool, optional
        :raises InvalidOperationError: [description]
        :raises InvalidOperationError: [description]
        """
        node = self.runtime.get_node(node_id)
        if node.type != NodeType.ServiceActivity:
            raise InvalidOperationError('{} is not activity, actual: {}'.format(node_id, node.type.value))
        state = self.runtime.get_state(node_id)
        if state.name != states.RUNNING:
            raise InvalidOperationError('{} state is not RUNNING, actual: {}'.format(node_id, state.name))
        process_id = self.runtime.get_process_id_with_current_node_id(node_id)
        if not process_id:
            raise InvalidOperationError('can not find process with current node id: {}'.format(node_id))
        self.runtime.pre_forced_fail_activity(node_id, ex_data)
        outputs = self.runtime.get_execution_data_outputs(node_id)
        outputs['ex_data'] = ex_data
        outputs['_forced_failed'] = True
        old_ver = state.version
        new_ver = self.runtime.set_state(node_id=node_id, to_state=states.FAILED, refresh_version=True, set_archive_time=True, send_post_set_state_signal=send_post_set_state_signal)
        self.runtime.set_execution_data_outputs(node_id, outputs)
        self.runtime.kill(process_id)
        self.runtime.post_forced_fail_activity(node_id, ex_data, old_ver, new_ver)

    def callback(self, node_id: str, version: str, data: dict):
        """
        回调某个节点

        :param node_id: 节点 ID
        :type node_id: str
        :param version: 回调执行版本
        :type version: str
        :param data: 回调数据
        :type data: dict
        :raises InvalidOperationError: [description]
        :raises InvalidOperationError: [description]
        :raises InvalidOperationError: [description]
        :raises InvalidOperationError: [description]
        """
        process_info = self.runtime.get_sleep_process_info_with_current_node_id(node_id)
        if not process_info:
            raise InvalidOperationError('can not find sleep process with current node id: {}'.format(node_id))
        state = self.runtime.get_state(node_id)
        schedule = self.runtime.get_schedule_with_node_and_version(node_id, version)
        if state.version != version:
            self.runtime.expire_schedule(schedule.id)
            raise InvalidOperationError('node version {} not exist'.format(version))
        if schedule.finished:
            raise InvalidOperationError('schedule is already finished')
        if schedule.expired:
            raise InvalidOperationError('schedule is already expired')
        self.runtime.pre_callback(node_id, version, data)
        data_id = self.runtime.set_callback_data(node_id, state.version, data)
        self.runtime.schedule(process_info.process_id, node_id, schedule.id, data_id)
        self.runtime.post_callback(node_id, version, data)

    @setup_gauge(ENGINE_RUNNING_PROCESSES)
    @setup_histogram(ENGINE_PROCESS_RUNNING_TIME)
    @interrupt_exception_catcher
    def execute(self, process_id: int, node_id: str, root_pipeline_id: str, parent_pipeline_id: str, interrupter: ExecuteInterrupter, headers: dict):
        """
        在某个进程上从某个节点开始进入推进循环

        :param process_id: 进程 ID
        :type process_id: int
        :param node_id: 节点 ID
        :type node_id: str
        :param root_pipeline_id: 根流程 ID
        :type root_pipeline_id: str
        :param parent_pipeline_id: 父流程 ID
        :type parent_pipeline_id: str
        """
        engine_pre_execute_start_at = time.time()
        if interrupter.recover_point:
            logger.info('[pipeline-trace](root_pipeline: %s) recover execute with point(%s)', root_pipeline_id, interrupter.recover_point.to_json())
        current_node_id = node_id
        with interrupter():
            process_info = self.runtime.get_process_info(process_id)
            self.runtime.wake_up(process_id)
            while True:
                interrupter.check(ExecuteKeyPoint.START_PUSH_NODE)
                ignore_boring_set = interrupter.recover_point is not None
                try:
                    self.runtime.beat(process_id)
                except Exception:
                    logger.exception('process(%s) beat error' % process_id)
                if current_node_id == process_info.destination_id:
                    wake_up_seccess = self.runtime.child_process_finish(process_info.parent_id, process_id)
                    if wake_up_seccess:
                        logger.info('[pipeline-trace](root_pipeline: %s) child(%s) wake up parent(%s) success', root_pipeline_id, process_id, process_info.parent_id)
                        self.runtime.execute(process_id=process_info.parent_id, node_id=process_info.destination_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id, headers=headers)
                    logger.info('[pipeline-trace](root_pipeline: %s) child(%s) wake up parent(%s) fail', root_pipeline_id, process_id, process_info.parent_id)
                    return
                logger.info('[pipeline-trace](root_pipeline: %s) execute node %s', root_pipeline_id, current_node_id)
                self.runtime.set_current_node(process_id, current_node_id)
                node_state_map = self.runtime.batch_get_state_name(process_info.pipeline_stack)
                if node_state_map[process_info.root_pipeline_id] == states.REVOKED:
                    self.runtime.die(process_id)
                    logger.info('[pipeline-trace](root_pipeline: %s) revoked checked at node %s', process_info.root_pipeline_id, current_node_id)
                    return
                for pid in process_info.pipeline_stack:
                    if node_state_map[pid] == states.SUSPENDED:
                        logger.info('[pipeline-trace](root_pipeline: %s) process %s suspended by subprocess %s', process_info.root_pipeline_id, process_id, pid)
                        self.runtime.suspend(process_id, pid)
                        return
                node = self.runtime.get_node(current_node_id)
                node_state = self.runtime.get_state_or_none(current_node_id)
                loop = 1
                inner_loop = 1
                reset_mark_bit = False
                if node_state:
                    if interrupter.recover_point and (not interrupter.recover_point.state_already_exist):
                        interrupter.check_and_set(ExecuteKeyPoint.SET_NODE_RUNNING_PRE_CHECK_DONE, state_already_exist=False)
                        if not interrupter.recover_point.running_node_version:
                            interrupter.recover_point.running_node_version = node_state.version
                    else:
                        interrupter.check_and_set(ExecuteKeyPoint.SET_NODE_RUNNING_PRE_CHECK_DONE, state_already_exist=True)
                        rerun_limit = self.runtime.node_rerun_limit(process_info.root_pipeline_id, current_node_id)
                        if node_state.name == states.FINISHED and node.type != NodeType.SubProcess and (node_state.loop > rerun_limit):
                            exec_outputs = self.runtime.get_execution_data_outputs(current_node_id)
                            exec_outputs['ex_data'] = 'node execution exceed rerun limit {}'.format(rerun_limit)
                            self.runtime.set_execution_data_outputs(current_node_id, exec_outputs)
                            self.runtime.sleep(process_id)
                            self.runtime.set_state(node_id=current_node_id, version=node_state.version, to_state=states.FAILED, set_archive_time=True, ignore_boring_set=ignore_boring_set)
                            return
                        if node_state.name == states.SUSPENDED:
                            self.runtime.set_state_root_and_parent(node_id=current_node_id, root_id=process_info.root_pipeline_id, parent_id=process_info.top_pipeline_id)
                            self.runtime.suspend(process_id, current_node_id)
                            logger.info('[pipeline-trace](root_pipeline: %s) process %s suspended by node %s', process_info.root_pipeline_id, process_id, current_node_id)
                            return
                        if node_state.name not in states.INVERTED_TRANSITION[states.RUNNING]:
                            logger.info('[pipeline-trace](root_pipeline: %s) can not transit state from %s to RUNNING for exist state', process_info.root_pipeline_id, node_state.name)
                            self.runtime.sleep(process_id)
                            return
                        if node_state.name == states.FINISHED:
                            loop = node_state.loop + 1
                            inner_loop = node_state.inner_loop + 1
                            reset_mark_bit = True
                            self._add_history(node_id=current_node_id, state=node_state)
                        else:
                            loop = node_state.loop
                            inner_loop = node_state.inner_loop
                else:
                    interrupter.check_and_set(ExecuteKeyPoint.SET_NODE_RUNNING_PRE_CHECK_DONE, state_already_exist=False)
                if interrupter.recover_point and interrupter.recover_point.running_node_version:
                    version = interrupter.recover_point.running_node_version
                else:
                    version = self.runtime.set_state(node_id=current_node_id, to_state=states.RUNNING, version=interrupter.recover_point.running_node_version if interrupter.recover_point else None, loop=loop, inner_loop=inner_loop, root_id=process_info.root_pipeline_id, parent_id=process_info.top_pipeline_id, set_started_time=True, reset_skip=reset_mark_bit, reset_retry=reset_mark_bit, reset_error_ignored=reset_mark_bit, refresh_version=reset_mark_bit, ignore_boring_set=ignore_boring_set)
                interrupter.check_and_set(ExecuteKeyPoint.SET_NODE_RUNNING_DONE, running_node_version=version)
                set_node_info(CurrentNodeInfo(node_id=current_node_id, version=version, loop=loop))
                logger.info('root pipeline[%s] before execute %s(%s) state: %s', process_info.root_pipeline_id, node.__class__.__name__, current_node_id, node_state)
                type_label = self._get_metrics_node_type(node)
                execute_start = time.time()
                if interrupter.recover_point and interrupter.recover_point.execute_result:
                    logger.info('root pipeline[%s] skip real execute node %s, using recover result', root_pipeline_id, node)
                    execute_result = interrupter.recover_point.execute_result
                else:
                    handler = HandlerFactory.get_handler(node, self.runtime, interrupter)
                    ENGINE_EXECUTE_PRE_PROCESS_DURATION.labels(type=node.type.value, hostname=self._hostname).observe(time.time() - engine_pre_execute_start_at)
                    execute_result = handler.execute(process_info=process_info, loop=loop, inner_loop=inner_loop, version=version, recover_point=interrupter.recover_point)
                engine_post_execute_start_at = time.time()
                interrupter.check_and_set(ExecuteKeyPoint.EXECUTE_NODE_DONE, execute_result=execute_result)
                logger.info('root pipeline[%s] node(%s) execute result: %s', process_info.root_pipeline_id, node.id, execute_result.__dict__)
                ENGINE_NODE_EXECUTE_TIME.labels(type=type_label, hostname=self._hostname).observe(time.time() - execute_start)
                if execute_result.should_sleep:
                    self.runtime.sleep(process_id)
                if execute_result.schedule_ready:
                    schedule = self.runtime.set_schedule(process_id=process_id, node_id=current_node_id, version=version, schedule_type=execute_result.schedule_type)
                    schedule_id = schedule.id
                    if execute_result.schedule_type == ScheduleType.POLL and (not interrupter.recover_point or not interrupter.recover_point.set_schedule_done):
                        self.runtime.schedule(process_id=process_id, node_id=current_node_id, schedule_id=schedule_id, headers=headers)
                    interrupter.check_and_set(ExecuteKeyPoint.EXECUTE_DONE_SET_SCHEDULE_DONE, set_schedule_done=True)
                elif execute_result.dispatch_processes:
                    children = [d.process_id for d in execute_result.dispatch_processes]
                    logger.info('root pipeline[%s] with top pipeline[%s] dispatch %s children: %s', process_info.root_pipeline_id, process_info.top_pipeline_id, len(execute_result.dispatch_processes), execute_result.dispatch_processes)
                    self.runtime.join(process_id, children)
                    for d in execute_result.dispatch_processes:
                        self.runtime.execute(process_id=d.process_id, node_id=d.node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id, headers=headers)
                if execute_result.should_die:
                    self.runtime.die(process_id)
                if execute_result.should_sleep or execute_result.should_die:
                    ENGINE_EXECUTE_POST_PROCESS_DURATION.labels(type=node.type.value, hostname=self._hostname).observe(time.time() - engine_post_execute_start_at)
                    return
                current_node_id = execute_result.next_node_id
                interrupter.to_node(current_node_id)
                ENGINE_EXECUTE_POST_PROCESS_DURATION.labels(type=node.type.value, hostname=self._hostname).observe(time.time() - engine_post_execute_start_at)

    @setup_gauge(ENGINE_RUNNING_SCHEDULES)
    @setup_histogram(ENGINE_SCHEDULE_RUNNING_TIME)
    @interrupt_exception_catcher
    def schedule(self, process_id: int, node_id: str, schedule_id: str, interrupter: ScheduleInterrupter, headers: dict, callback_data_id: Optional[int]=None):
        """
        在某个进程上开始某个节点的调度

        :param process_id: 进程 ID
        :type process_id: int
        :param node_id: 节点 ID
        :type node_id: str
        :param schedule_id: 调度对象 ID
        :type schedule_id: str
        :param callback_data_id: 回调数据 ID, defaults to None
        :type callback_data_id: Optional[int], optional
        """
        engine_pre_schedule_start_at = time.time()
        if interrupter.recover_point:
            logger.info('[pipeline-trace](schedule: %s) recover schedule with point(%s)', schedule_id, interrupter.recover_point.to_json())
        root_pipeline_id = ''
        with interrupter():
            process_info = self.runtime.get_process_info(process_id)
            root_pipeline_id = process_info.root_pipeline_id
            state = self.runtime.get_state(node_id)
            schedule = self.runtime.get_schedule(schedule_id)
            set_node_info(CurrentNodeInfo(node_id=node_id, version=state.version, loop=state.loop))
            if schedule.finished:
                logger.warning('root pipeline[%s] schedule(%s) %s with version %s already finished', root_pipeline_id, schedule_id, node_id, schedule.version)
                return
            version_mismatch = False
            if interrupter.recover_point and interrupter.recover_point.version_mismatch is not None:
                version_mismatch = interrupter.recover_point.version_mismatch
            elif state.version != schedule.version:
                version_mismatch = True
            interrupter.check_and_set(ScheduleKeyPoint.VERSION_MISMATCH_CHECKED, version_mismatch=version_mismatch)
            if version_mismatch:
                logger.info('root pipeline[%s] schedule(%s) %s with version %s expired, current version: %s', root_pipeline_id, schedule_id, node_id, schedule.version, state.version)
                self.runtime.expire_schedule(schedule_id)
                return
            node_not_running = False
            if interrupter.recover_point and interrupter.recover_point.node_not_running is not None:
                node_not_running = interrupter.recover_point.node_not_running
            elif state.name != states.RUNNING:
                node_not_running = True
            interrupter.check_and_set(ScheduleKeyPoint.NODE_NOT_RUNNING_CHECKED, node_not_running=node_not_running)
            if node_not_running:
                logger.info('root pipeline[%s] schedule(%s) %s with version %s state is not running: %s', root_pipeline_id, schedule_id, node_id, schedule.version, state.name)
                self.runtime.expire_schedule(schedule_id)
                return
            if interrupter.recover_point and interrupter.recover_point.lock_get is not None:
                lock_get = interrupter.recover_point.lock_get
            else:
                lock_get = self.runtime.apply_schedule_lock(schedule_id)
            interrupter.check_and_set(ScheduleKeyPoint.APPLY_LOCK_DONE, lock_get=lock_get)
            if not lock_get:
                if schedule.type is not ScheduleType.MULTIPLE_CALLBACK:
                    logger.info('root pipeline[%s] schedule(%s) %s with version %s is not multiple callback type, will not retry to get lock', root_pipeline_id, schedule_id, node_id, schedule.version)
                    return
                try_after = random.randint(1, 5)
                logger.info('root pipeline[%s] schedule(%s) lock %s with data %s fetch fail, try after %s', root_pipeline_id, node_id, schedule_id, callback_data_id, try_after)
                self.runtime.set_next_schedule(process_id=process_id, node_id=node_id, schedule_id=schedule_id, callback_data_id=callback_data_id, schedule_after=try_after, headers=headers)
                return
            logger.info('[pipeline-trace](root_pipeline: %s) schedule node %s with version %s' % (root_pipeline_id, node_id, schedule.version))
            try:
                self.runtime.beat(process_id)
            except Exception:
                pass
            callback_data = None
            if callback_data_id:
                callback_data = self.runtime.get_callback_data(callback_data_id)
            node = self.runtime.get_node(node_id)
            type_label = self._get_metrics_node_type(node)
            logger.info('root pipeline[%s] before schedule node %s with data %s', root_pipeline_id, node, callback_data)
            schedule_start = time.time()
            if interrupter.recover_point and interrupter.recover_point.schedule_result:
                logger.info('root pipeline[%s] skip real schedule node %s, using recover result', root_pipeline_id, node)
                schedule_result = interrupter.recover_point.schedule_result
            else:
                handler = HandlerFactory.get_handler(node, self.runtime, interrupter)
                ENGINE_SCHEDULE_PRE_PROCESS_DURATION.labels(type=node.type.value, hostname=self._hostname).observe(time.time() - engine_pre_schedule_start_at)
                schedule_result = handler.schedule(process_info=process_info, loop=state.loop, inner_loop=state.inner_loop, schedule=schedule, callback_data=callback_data, recover_point=interrupter.recover_point)
            engine_post_schedule_start_at = time.time()
            interrupter.check_and_set(ScheduleKeyPoint.SCHEDULE_NODE_DONE, schedule_result=schedule_result)
            ENGINE_NODE_SCHEDULE_TIME.labels(type=type_label, hostname=self._hostname).observe(time.time() - schedule_start)
            logger.info('root pipeline[%s] node(%s) schedule result: %s', process_info.root_pipeline_id, node.id, schedule_result.__dict__)
            if not interrupter.recover_point or not interrupter.recover_point.lock_released:
                self.runtime.release_schedule_lock(schedule_id)
            interrupter.check_and_set(ScheduleKeyPoint.RELEASE_LOCK_DONE, lock_released=True)
            if schedule_result.has_next_schedule:
                self.runtime.set_next_schedule(process_id=process_info.process_id, node_id=node_id, schedule_id=schedule_id, schedule_after=schedule_result.schedule_after, headers=headers)
            if schedule_result.schedule_done:
                self.runtime.finish_schedule(schedule_id)
                self.runtime.execute(process_id=process_id, node_id=schedule_result.next_node_id, root_pipeline_id=process_info.root_pipeline_id, parent_pipeline_id=process_info.top_pipeline_id, headers=headers)
            ENGINE_SCHEDULE_POST_PROCESS_DURATION.labels(type=node.type.value, hostname=self._hostname).observe(time.time() - engine_post_schedule_start_at)

    def _add_history(self, node_id: str, state: Optional[State]=None, exec_data: Optional[ExecutionData]=None) -> int:
        if not state:
            state = self.runtime.get_state(node_id)
        if not exec_data:
            try:
                exec_data = self.runtime.get_execution_data(node_id)
            except NotFoundError:
                logger.warning("can't not find execution data for {} at loop {}".format(node_id, state.loop))
                history_inputs = {}
                history_outputs = {}
            else:
                history_inputs = exec_data.inputs
                history_outputs = exec_data.outputs
        return self.runtime.add_history(node_id=node_id, started_time=state.started_time, archived_time=state.archived_time, loop=state.loop, skip=state.skip, retry=state.retry, version=state.version, inputs=history_inputs, outputs=history_outputs)

    def _ensure_state_is_fail_and_return_process_info(self, state: State) -> str:
        if state.name != states.FAILED:
            raise InvalidOperationError('{} state is not FAILED, actual {}'.format(state.node_id, state.name))
        process_info = self.runtime.get_sleep_process_info_with_current_node_id(state.node_id)
        if not process_info:
            raise InvalidOperationError('can not find sleep process with current node id: {}'.format(state.node_id))
        return process_info

    def _get_metrics_node_type(self, node: Node) -> str:
        if node.type != NodeType.ServiceActivity:
            return get_lower_case_name(node.type.value)
        return '{}_{}'.format(node.code, node.version)