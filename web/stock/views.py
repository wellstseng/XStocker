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
    logger.info("check task {} status".format(task))
    filt = TaskResult.objects.filter(task_id=task)
    logger.info("result: {}".format(filt))
    if len(filt) > 0:
        result = filt[0]    
        if result.status == "PENDING":
            new_dic = {"status":result.status}
        else:
            tbl = xstocker.get_predict_price2(stock_id)  
            new_dic = {"status":result.status, "stock_id": stock_id, "value":tbl}
    else:
        new_dic = {"status":"PENDING", "stock_id": stock_id}
    return JsonResponse(new_dic)

def init(request):    
    logger.info("init:" + str(request.POST) + " user " + str(request.user))
    dic = request.POST.dict()
    stock_id = dic["stock_name"].replace("s_","")

    json_tbl = {"status":"INIT",  "stock_id":stock_id, "task":None, "value":None}
    if xstocker.check_res_has_per_pbr_data(stock_id):        
        predict_price_tbl = xstocker.get_predict_price2(stock_id)
        logger.info("has data in db:"+ stock_id + "price tbl: " + str(predict_price_tbl))
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