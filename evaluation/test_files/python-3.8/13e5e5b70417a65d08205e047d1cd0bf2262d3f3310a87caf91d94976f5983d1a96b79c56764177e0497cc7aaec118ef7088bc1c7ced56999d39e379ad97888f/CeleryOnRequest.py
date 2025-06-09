import logging
from celery.signals import task_revoked
from api.model.ResultVO import ResultVO, FAIL_CODE
from cloudcelery import celery
from cloudcelery import celery_redis_client
from schedule import TriggerActor
from munch import Munch
import json
log = logging.getLogger('Ficus')

def checkTaskRepetition(task_id) -> bool:
    """
    判断从celery里面获取到的任务是否重复.
    celery使用redis作为后端的时候,会有一个visibility_timeout来控制任务时候超时未完成.
    但是他自己本身的原因, 就算把visibility_timeout设置成了12小时,他还是有可能会把任务重新触发.这是不满足我们要求的.
    所以,就只能自己想办法了,也就是使用 redis中的 SETNX来加锁. 执行过的就不再执行了(12小时过期)
    :return: 如果已经重复了,返回True,  否则返回False
    """
    redis = celery_redis_client()
    key = f'sobeyficus.celery.repetition.{task_id}'
    if redis.setnx(key, '1'):
        redis.expire(key, 43200)
        return False
    return True

@celery.task(name='tasks.on_request', bind=True, max_retries=2, default_retry_delay=1 * 6)
def on_request(self, protocol):
    """
    从celery接收协议
    :param self:
    :param protocol:
    :return:
    """
    log.info(f'从celery中获取到任务:{protocol}')
    body = Munch(json.loads(protocol))
    if checkTaskRepetition(body.logId):
        log.info(f'从celery中获取的任务:logId:{body.logId} 已经被执行过,12小时内不再重复执行.')
        return {'status': True, 'data': {'code': 2, 'msg': 'success', 'content': None}}
    try:
        from discovery import discovery_service_proxy
        import config
        discovery_service_proxy().registry_discovery(config.eureka_default_zone, renewal_interval_in_secs=4)
    except:
        pass
    try:
        from factdatasource import FactDatasourceProxyService
        FactDatasourceProxyService.fd_client_proxy()
        log.info('完成FD服务监听加载')
    except:
        pass
    result: ResultVO = TriggerActor.handle_trigger(body, True)
    log.info(f'任务执行完成，jobId:{body.jobId} logId:{body.logId}')
    if result.code == FAIL_CODE:
        raise RuntimeError(result.msg)
    return {'status': True, 'data': result.to_dict()}

@task_revoked.connect(sender=on_request, dispatch_uid='cloudcelery.CeleryOnRequest.on_request')
def on_revoke(request=None, terminated=None, signum=None, expired=None, **kwargs):
    if str(signum) != 'Signals.SIGKILL':
        return
    log.info(f'celery服务器:{request.hostname} 接收到任务:{request.id} 的取消事件(terminated:{terminated},expired:{expired})')
    log_id = request.reply_to
    try:
        from handlers import revoke_handler
    except Exception as e:
        return
    try:
        from discovery import discovery_service_proxy
        import config
        discovery_service_proxy().registry_discovery(config.eureka_default_zone, renewal_interval_in_secs=4)
    except:
        pass
    from client import ScheduleJobTaskLogClient
    from api.handler.ICacheAbleHandler import CacheAbleHandlerHolder
    task_log = ScheduleJobTaskLogClient.get_task_log_by_id(log_id)
    try:
        actorParam = Munch(json.loads(task_log.actorParam))
        CacheAbleHandlerHolder.get_handler().set_local_code(actorParam['site_'] + '_' + actorParam['projectCode_'] + '_' + actorParam['code_'])
        CacheAbleHandlerHolder.get_handler().set_process_id(actorParam.get('__processLogId__'))
        revoke_handler(task_log.actorCode, task_log.actorHandler, actorParam['code_'], actorParam['projectCode_'], actorParam['site_'], task_log.id, task_log.jobId, task_log.messageId, expired)
    except Exception as e:
        log.warning(f'任务:{task_log},取消回调失败:{str(e)}')