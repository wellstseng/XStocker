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
       

