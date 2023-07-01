import time
from celery import Celery
from netcore.config import settings

celery = Celery(__package__)
celery.conf.broker_url = settings.celery.broker_url
celery.conf.result_backend = settings.celery.result_backend

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True