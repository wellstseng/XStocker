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
from resonable_price import resonable_price


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
                tbl = {}
                logger.info(str(record))
                stock_id = str(record)               
                tbl["tock_id"] = stock_id
                #TODO 合理價存入mongo db 
                df = None#resonable_price.execute(stock_id)
                if df is not None:
                    tbl["expensive"] =  df.iloc[0, [0]].values[0]
                    tbl["resonable"] =  df.iloc[0, [1]].values[0]
                    tbl["cheap"] =  df.iloc[0, [2]].values[0]             
                sett[str(stock_id)] = tbl
        return sett
       

