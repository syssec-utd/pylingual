from __future__ import absolute_import
import os
import logging
from celery import Celery
from celery import platforms
from django.conf import settings
from easypush.core.mq.context import ContextTask
from .celeryconf import CeleryConfig
__all__ = ['app', 'celery_app']
logging.warning('Celery use `DJANGO_SETTINGS_MODULE` config: %s' % os.getenv('DJANGO_SETTINGS_MODULE'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easypush_demo.settings')
app = Celery(settings.APP_NAME + '_celery', task_cls=ContextTask)
app.set_current()
platforms.C_FORCE_ROOT = True
app.config_from_object(obj=CeleryConfig)
celery_app = app

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))