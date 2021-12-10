from celery import Celery
from settings import RABBIT_MQ_URL


app = Celery('app', broker=f'pyamqp://{RABBIT_MQ_URL}//', include=['consumer.tasks'])

