from django.urls import path

from . import views
from django.conf.urls import url
from django.views.generic import TemplateView
app_name = "resume"
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='resume/index.html')),
]