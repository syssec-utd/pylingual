from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.http.response import JsonResponse
from django.conf import settings
from . import serializers, get_task_model, get_schedule_log_model, get_task_schedule_model, get_task_schedule_serializer
from .choices import TaskScheduleStatus
from .models import TaskSchedule, TaskScheduleProducer, TaskScheduleQueue, ConsumerPermission, ExceptionReport, builtins, ScheduleConfig
from django_common_objects.rest_view import UserListAPIView, UserRetrieveAPIView
from django.views.decorators.csrf import csrf_exempt
from queue import Empty
from datetime import datetime
from jionlp_time import parse_time
from .utils.schedule_time import nlp_config_to_schedule_config
from .models import system_initialize_signal, system_schedule_event
from threading import Thread
import time
import traceback
TaskModel = get_task_model()
ScheduleLogModel = get_schedule_log_model()
ScheduleModel = get_task_schedule_model()
ScheduleSerializer = get_task_schedule_serializer()
builtins.initialize()

class TaskScheduleThread(Thread):
    schedule_model = ScheduleModel
    producers = builtins.producers
    queues = builtins.queues
    serializer = ScheduleSerializer

    def __init__(self):
        super().__init__(daemon=True)

    def produce(self):
        now = datetime.now()
        qsize = getattr(settings, 'SCHEDULE_QUEUE_MAX_SIZE', 1000)
        max_queue_size = qsize * 2
        for producer in self.producers.values():
            queue_instance = self.queues[producer.queue.code]
            queue = queue_instance.queue
            if queue.qsize() >= qsize:
                continue
            queryset = self.schedule_model.objects.filter(**producer.filters)
            if producer.lte_now:
                queryset = queryset.filter(next_schedule_time__lte=now)
            for schedule in queryset:
                try:
                    while queue.qsize() < max_queue_size and schedule.next_schedule_time <= now:
                        data = self.serializer(schedule).data
                        data['queue'] = queue_instance.code
                        queue.put(data)
                        schedule.next_schedule_time = ScheduleConfig(config=schedule.config).get_next_time(schedule.next_schedule_time)
                    schedule.save(update_fields=('next_schedule_time',))
                except Exception as e:
                    schedule.status = TaskScheduleStatus.ERROR.value
                    schedule.save(update_fields=('status',))
                    traceback.print_exc()

    def run(self) -> None:
        system_schedule_event.wait(timeout=5)
        SCHEDULE_INTERVAL = getattr(settings, 'SCHEDULE_INTERVAL', 1)
        while True:
            try:
                self.produce()
            except Exception as err:
                traceback.print_exc()
            time.sleep(SCHEDULE_INTERVAL)

@receiver(system_initialize_signal, sender='system_initialized')
def on_system_initialized(sender, **kwargs):
    thread = TaskScheduleThread()
    thread.start()

@receiver(post_delete, sender=TaskScheduleQueue)
def delete_queue(sender, instance: TaskScheduleQueue, **kwargs):
    builtins.queues.delete(instance)

@receiver(post_save, sender=TaskScheduleQueue)
def add_queue(sender, instance: TaskScheduleQueue, created, **kwargs):
    builtins.queues.add(instance)

@receiver(post_save, sender=TaskScheduleProducer)
def add_producer(sender, instance: TaskScheduleProducer, created, **kwargs):
    builtins.producers.add(instance)

@receiver(post_delete, sender=TaskScheduleProducer)
def delete_producer(sender, instance: TaskScheduleProducer, **kwargs):
    builtins.producers.delete(instance)

@receiver(post_save, sender=ConsumerPermission)
def add_consumer_permission(sender, instance: ConsumerPermission, created, **kwargs):
    builtins.consumer_permissions.add(instance)

@receiver(post_delete, sender=ConsumerPermission)
def delete_consumer_permission(sender, instance: ConsumerPermission, **kwargs):
    builtins.consumer_permissions.delete(instance)

class TaskListView(UserListAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = serializers.TaskSerializer

class TaskDetailView(UserRetrieveAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = serializers.TaskSerializer

class TaskScheduleListView(UserListAPIView):
    queryset = TaskSchedule.objects.all()
    serializer_class = serializers.TaskScheduleSerializer

class TaskScheduleDetailView(UserRetrieveAPIView):
    queryset = TaskSchedule.objects.all()
    serializer_class = serializers.TaskScheduleSerializer

class ScheduleLogViewSet(ModelViewSet):
    queryset = ScheduleLogModel.objects.all()
    serializer_class = serializers.TaskScheduleLogSerializer

class TaskScheduleQueueAPI(object):
    queues = builtins.queues
    consumer_permissions = builtins.consumer_permissions
    schedule_model = TaskSchedule
    log_model = ScheduleLogModel
    serializer = ScheduleSerializer
    permission_validator = None

    @classmethod
    def get(cls, request: Request, code: str):
        instance = cls.queues.get(code, None)
        if instance is None:
            return JsonResponse({'error': '队列(%s)不存在' % code}, status=status.HTTP_404_NOT_FOUND)
        permission_validator = cls.permission_validator or cls.consumer_permissions.get(code, None)
        if permission_validator is not None:
            error = permission_validator.validate(request)
            if error:
                return JsonResponse({'error': error}, status=status.HTTP_403_FORBIDDEN)
        try:
            task = instance.queue.get_nowait()
        except Empty:
            return JsonResponse({'message': 'no schedule for %s' % code}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return JsonResponse({'error': 'get schedule error: %s' % e}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(task)

    @classmethod
    def get_by_id(cls, request, pk):
        try:
            schedule = cls.schedule_model.objects.get(id=pk)
            return Response(cls.serializer(schedule).data)
        except TaskSchedule.DoesNotExist:
            return Response({'error': 'schedule not found'}, status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def retry(cls, request):
        log_ids = request.GET.get('log-ids', None)
        if not log_ids:
            return JsonResponse({'error': 'log-ids不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            log_ids = [int(i) for i in log_ids.split(',')]
            assert len(log_ids) < 1000, 'log-ids不能超过1000个'
        except Exception as e:
            return JsonResponse({'error': 'logs_ids参数错误: %s' % e}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = {x: 'no such log' for x in log_ids}
            logs = cls.log_model.objects.filter(id__in=log_ids)
            for log in logs:
                queue = cls.queues[log.queue].queue
                log.schedule.next_schedule_time = log.schedule_time
                log.schedule.generator = 'retry'
                data = cls.serializer(log.schedule).data
                data['queue'] = log.queue
                queue.put(data)
                result[log.id] = log.queue
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': '重试失败: %s' % e}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    @csrf_exempt
    def put(cls, request: Request):
        schedule_ids = request.GET.get('i', None) or request.POST.get('i', None)
        queues = request.GET.get('q', None) or request.POST.get('q', None)
        schedule_times = request.GET.get('t', None) or request.POST.get('t', None)
        if not schedule_ids or not queues or (not schedule_times):
            return JsonResponse({'error': 'schedule_ids(i)、queues(q)、schedule_times(t)不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            schedule_ids = [int(i) for i in schedule_ids.split(',')]
            queues = [i.strip() for i in queues.split(',')]
            schedule_times = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in schedule_times.split(',')]
            assert len(schedule_ids) <= 1000, '不能超过1000个'
            if len(queues) == 1:
                q = queues[0]
                queues = [q for _ in schedule_ids]
            elif len(queues) != len(schedule_ids):
                raise Exception('ids和queues长度不一致')
            if len(schedule_times) == 1:
                t = schedule_times[0]
                schedule_times = [t for _ in schedule_ids]
            elif len(schedule_times) != len(schedule_ids):
                raise Exception('ids和schedule_times长度不一致')
        except Exception as e:
            return JsonResponse({'error': 'ids参数错误: %s' % e}, status=status.HTTP_400_BAD_REQUEST)
        try:
            schedules = cls.schedule_model.objects.filter(id__in=set(schedule_ids))
            schedule_mapping = {x.id: x for x in schedules}
            result = {}
            for (i, q, t) in zip(schedule_ids, queues, schedule_times):
                queue_instance = cls.queues.get(q, None)
                if queue_instance is None:
                    result[q] = 'no such queue: %s' % q
                    continue
                queue_result = result.setdefault(q, {})
                schedule = schedule_mapping.get(i, None)
                if schedule is None:
                    queue_result[i] = 'no such schedule: %s' % i
                    continue
                schedule_result = queue_result.setdefault(i, [])
                schedule.next_schedule_time = t
                schedule.generator = 'put'
                data = cls.serializer(schedule).data
                data['queue'] = q
                queue_instance.queue.put(data)
                schedule_result.append(t.strftime('%Y-%m-%d %H:%M:%S'))
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': '添加到队列失败: %s' % e}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def status(cls, request):
        return JsonResponse({x: y.queue.qsize() for (x, y) in cls.queues.items()})

class ScheduleTimeParseView(APIView):

    def get(self, request, *args, **kwargs):
        sentence = request.query_params.get('sentence')
        if not sentence:
            return Response({'error': 'sentence is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = parse_time(sentence)
            schedule = nlp_config_to_schedule_config(result, sentence=sentence)
            return Response({'jio_result': result, 'schedule': schedule})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExceptionReportView(CreateAPIView):
    queryset = ExceptionReport.objects.all()
    serializer_class = serializers.ExceptionSerializer

    def perform_create(self, serializer):
        meta = self.request.META
        ip = meta.get('HTTP_X_FORWARDED_FOR') if meta.get('HTTP_X_FORWARDED_FOR') else meta.get('REMOTE_ADDR')
        serializer.save(ip=ip)