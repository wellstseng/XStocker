# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import sys, os

try:
    from web.web.settings import BASE_DIR
except:
    from web.settings import BASE_DIR
sys.path.append(os.path.join(os.path.dirname(BASE_DIR),"src"))
print(sys.path)
from predict_price import db_manager

@shared_task
def add(x, y):
    return x + y


@shared_task
def load_predict_price(stock_id):
    return db_manager.fetch_predict_price(stock_id)