#²��
�ϥ�Django�إߤ��ӤH����
�n�J��i�d�߭ӪѦX�z����

##�\��
1. �����C�ѤU��6�I����}�������ҥ�һP�d�R���ߤ��C�馬�L��Ƥ��R�æs�JmongoDB��Ʈw
2. �U��GoodInfo�ӪѸg���Z�ĭp��X�z����
3. ����ӪѦ��L���P�X�z�������Y�ѨϥΪ̰Ѧ�


# ���һݨD
## �@�~�t�� 
CentOS7

## ��Ʈw����
MongoDB

## �ݨD�A��
python3.6.6
pip3.6
nginx
rabbitmq

#�G�p
## instance 1
nginx
python3.6.6
celery

## instance 2
mongoDB

#���O
## Django����
cd web
python .\manage.py runserver

## Celery
cd web
python3 -m celery -A web worker [--detach] -l info -P eventlet(�`�Npermission)

## ����uwsgi
sudo pkill -f uwsgi -9