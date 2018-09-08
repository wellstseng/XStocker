from django.urls import path

from . import views
app_name = "stock"
urlpatterns = [
    path('overview/', views.RecordOverview.as_view(), name='overview'),
    path('test/', views.test, name='test'),
    path('query/', views.query, name='query'),
    path('test_celery/', views.test_celery, name='test_celery'),
    path('init/', views.init, name='init'),
    #path('update_price/', views.update_price, name='update_price')
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]