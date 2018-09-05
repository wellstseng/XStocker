from django.shortcuts import render
from django.views import generic
from django.http import  HttpResponse
from .models import Overview
from django_celery_results.models import TaskResult
import logging
logger = logging.getLogger('django')

# CUSTOME import project path
import sys,os
from web.settings import BASE_DIR
sys.path.append(os.path.join(os.path.dirname(BASE_DIR),"src"))
import xstocker

import asyncio

class RecordOverview(generic.ListView):
    template_name="stock/overview.html"
    context_object_name='dataset'
    
    def get_queryset(self):
        current_user = self.request.user
        results = Overview.objects.filter(user_id=current_user.id)

        sett = None
        userdata = results[0] if len(results) > 0 else None
        if userdata != None:        
            sett = {}   
            for record in userdata.stock_list: 
                stock_id = str(record)
                json_tbl = {"status":"INIT",  "data":None, "task":None}
                if xstocker.check_db_has_predict_price(stock_id):
                    logger.info("has data in db:"+ stock_id)
                    predict_price_tbl = xstocker.get_stock_info(stock_id)
                    json_tbl["status"] = "SUCCESS"
                    json_tbl["data"] = predict_price_tbl
                else:
                    logger.info("load {} async".format(stock_id))
                    task = load_predict_price.delay(stock_id)
                    json_tbl["status"] = task.status
                    json_tbl["task_id"] = task.task_id
                sett[stock_id] = json_tbl
                
        return sett
    
from django.http import JsonResponse
def test(request):
    return render(request, "stock/test.html")

from django.views.decorators.csrf import csrf_exempt
import time

@csrf_exempt
def query(request):    
    logger.info("request:" + str(request.POST))
    dic = request.POST.dict()
    stock_id = dic["stock_name"].replace("s_","")
    task = dic["task_id"]
    logger.info("check task {} status".format(task))
    filt = TaskResult.objects.filter(task_id=task)
    logger.info("result: {}".format(filt))
    if len(filt) > 0:
        result = filt[0]    
        if result.status == "PENDING":
            new_dic = {"status":result.status}
        else:
            tbl = xstocker.get_stock_info(stock_id)  
            new_dic = {"status":result.status, "stock_id": stock_id, "value":tbl}
    else:
        new_dic = {"status":"PENDING"}
    return JsonResponse(new_dic)


from .tasks import load_predict_price
def test_celery(request):
    logger.info("test celery1")    
    result = load_predict_price.delay("2458")
    return HttpResponse(result.task_id)