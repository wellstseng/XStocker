from django.shortcuts import render
from django.views import generic
from django.http import  HttpResponse
from .models import Overview
import logging
logger = logging.getLogger('django')

class RecordOverview(generic.ListView):
    template_name="stock/overview.html"
    context_object_name='object_list'
    
    def get_queryset(self):
        current_user = self.request.user
        results = Overview.objects.filter(user_id=current_user.id)
        return results
       

