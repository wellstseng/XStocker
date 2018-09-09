#啟動服務
## Django
cd web
python .\manage.py runserver

## Celery
cd web
celery -A web worker -l info -P eventlet