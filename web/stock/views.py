from django.shortcuts import render
from django.views import generic
from django.http import  HttpResponse
from .models import Overview
import logging
logger = logging.getLogger('django')

# CUSTOME import project path
import sys,os
from web.settings import BASE_DIR
sys.path.append(os.path.join(os.path.dirname(BASE_DIR),"src"))
import xstocker


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
                tbl = xstocker.get_stock_info(stock_id)           
                sett[stock_id] = tbl
                
        return sett
    
from django.http import JsonResponse
def test(request):
    return render(request, "stock/test.html")

from django.views.decorators.csrf import csrf_exempt
import time

cache = {}
def _delay(d):
    time.sleep(2+d*1.5)
    logger.info("delay 5 finish")
    return HttpResponse("hello  1234567")


@csrf_exempt
def query(request):    
    logger.info("request:" + str(request.POST))
    dic = request.POST.dict()
    stock_id = dic["stock_name"].replace("s_","")
    tbl = xstocker.get_stock_info(stock_id)  
    new_dic = {"stock_id": stock_id, "value":tbl}
    return JsonResponse(new_dic)

from .tasks import *
def test_celery(request):
    logger.info("test celery")
    xstocker.get_stock_info("2377")
    return HttpResponse("hello")