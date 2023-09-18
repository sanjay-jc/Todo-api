from __future__ import absolute_import,unicode_literals
from celery.utils.log import get_task_logger
from celery import shared_task

# @shared_task
# def add(x,y):
#     return x+y

logger =get_task_logger(__name__)

from .email import send_email

@shared_task(name='send_email_task')
def send_email_task(name,email,review):
    logger.info(f"{name},{email},{review}")
    return send_email(name,email,review)