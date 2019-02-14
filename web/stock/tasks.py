# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import sys, os
from celery.signals import task_success

try:
    from web.web.settings import BASE_DIR
except:
    from web.settings import BASE_DIR
print("task path: " + str(sys.path))
try:
    from predict_price import manager
except:
    from src.predict_price import manager

cnt = 0

@shared_task
def add(x, y):
    return x + y


@shared_task
def load_predict_price(stock_id):
    print("sleep 10")
    time.sleep(10)
    #db_manager.fetch_predict_price(stock_id)
    manager.execute(stock_id, None, True)
    print("sleep 10 finsidh !!!!@@@@@!@")
    
    return stock_id

@shared_task
def load_per_pbr_data(stock_id):
    print("load per pbr data")

    manager.load_per_pbr_data(stock_id, True, True)
    
    print("***** load finsidh !!!!@@@@@!@  " + stock_id)
    
    return stock_id

from django.http import  HttpResponse
@task_success.connect
def on_success(sender, result, **kwargs):
    print("on success")
