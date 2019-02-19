# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import sys, os
from celery.signals import task_success
from django.http import  HttpResponse

try:
    from web.web.settings import BASE_DIR
except:
    from web.settings import BASE_DIR
try:
    from predict_price import manager
except:
    from src.predict_price import manager

@shared_task
def load_predict_price(stock_id):
    #db_manager.fetch_predict_price(stock_id)
    manager.execute(stock_id, None, True)    
    return stock_id

@shared_task
def load_per_pbr_data(stock_id):
    manager.load_per_pbr_data(stock_id, True, True)   
    return stock_id

@task_success.connect
def on_success(sender, result, **kwargs):
    pass
