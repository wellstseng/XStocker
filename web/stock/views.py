import sys,os
from web.settings import BASE_DIR
sys.path.append(os.path.join(os.path.dirname(BASE_DIR),"src"))

from django.shortcuts import render
from django.views import generic
from django.http import  HttpResponse, JsonResponse
from .models import Overview
from django_celery_results.models import TaskResult
from .tasks import load_per_pbr_data
import logging    
import time
logger = logging.getLogger('django')

# CUSTOME import project path
import xstocker

import asyncio

class RecordOverview(generic.ListView):
    template_name="stock/overview.html"
    context_object_name='dataset'
    
    def get_queryset(self):
        current_user = self.request.user
        userdata = None
        if current_user:
            results = Overview.objects.filter(user_id=current_user.id)
            userdata = results[0] if len(results) > 0 else None

        sett = {}
        stk_list=None
        
        if userdata != None:    
            stk_list = userdata.stock_list
        else:
            stk_list={2377, 3546, 3324, 2317,1201,2492,1477,2610} #TODO 讀外部清單
        for record in stk_list:
            stock_id = str(record)
            json_tbl = {"status":"INIT",  "data":None, "task":None, "basic":None}
            json_tbl["basic"] = xstocker.get_basic_info(stock_id)
            if xstocker.check_res_has_per_pbr_data(stock_id):                   
                json_tbl["status"] = "INIT"
                pass
            else:
                logger.info("load {} async".format(stock_id))
                task = load_per_pbr_data.delay(stock_id)
                json_tbl["status"] = task.status
                json_tbl["task_id"] = task.task_id
            sett[stock_id] = json_tbl       
        return sett


def query(request):    
    logger.info("@query request:" + str(request.POST))
    dic = request.POST.dict()
    stock_id = dic["stock_name"].replace("s_","")
    task = dic["task_id"]
    quarter = dic["quarter"] if "quarter" in dic else None
    logger.info("check task {} status   quarter {}".format(task, str(quarter)))
    filt = TaskResult.objects.filter(task_id=task)
    logger.info("result: {}".format(filt))
    if len(filt) > 0:
        result = filt[0]    
        if result.status == "PENDING":
            new_dic = {"status":result.status}
        else:
            tbl = xstocker.get_predict_price2(stock_id, quarter)  
            new_dic = {"status":result.status, "stock_id": stock_id, "value":tbl}
    else:
        new_dic = {"status":"PENDING", "stock_id": stock_id}
    return JsonResponse(new_dic)

def init(request):    
    logger.info("init:" + str(request.POST) + " user " + str(request.user))
    dic = request.POST.dict()
    stock_id = dic["stock_name"].replace("s_","")
    quarter = dic["quarter"] if "quarter" in dic else None
    date_time = dic["date_time"] if "date_time" in dic else None
    json_tbl = {"status":"INIT",  "stock_id":stock_id, "task":None, "value":None, "basic":None}
    json_tbl["basic"] = xstocker.get_basic_info(stock_id, date_time)
    if xstocker.check_res_has_per_pbr_data(stock_id):        
        predict_price_tbl = xstocker.get_predict_price2(stock_id, quarter)
        logger.info("has data in db:"+ stock_id + "price tbl: " + str(predict_price_tbl) + " quarter: " + str(quarter))
        json_tbl["status"] = "SUCCESS"
        json_tbl["value"] = predict_price_tbl
    else:
        logger.info("load {} async".format(stock_id))
        task = load_per_pbr_data.delay(stock_id)
        json_tbl["status"] = task.status
        json_tbl["task"] = task.task_id

    current_user = request.user
    results = Overview.objects.filter(user_id=current_user.id)
    userdata = results[0] if len(results) > 0 else None
    if userdata != None and not userdata.has_stock(stock_id):
        logger.info("add stock " + stock_id)
        userdata.add_stock(stock_id)
        

    return JsonResponse(json_tbl)

def delete_stock(request):
    logger.info("delete :" + str(request.POST) + " user " + str(request.user))
    dic = request.POST.dict()
    stock_id = dic["stock_id"]
    json_tbl = {"status":"SUCCESS",  "stock_id":stock_id}
    current_user = request.user
    results = Overview.objects.filter(user_id=current_user.id)
    userdata = results[0] if len(results) > 0 else None
    if userdata != None and userdata.has_stock(stock_id):
        logger.info("remove stock " + stock_id)
        success = userdata.remove_stock(stock_id)
        if not success:
            json_tbl["status"] == "FAILURE"
    return JsonResponse(json_tbl)
