#簡介
使用Django建立之個人網頁
登入後可查詢個股合理價格

##功能
1. 本機每天下午6點執行腳本爬取證交所與櫃買中心之每日收盤資料分析並存入mongoDB資料庫
2. 下載GoodInfo個股經營績效計算合理價格
3. 比較個股收盤價與合理價之關係供使用者參考


# 環境需求
## 作業系統 
CentOS7

## 資料庫環境
MongoDB

## 需求服務
python3.6.6
pip3.6
nginx
rabbitmq

#佈署
## instance 1
nginx
python3.6.6
celery

## instance 2
mongoDB

#指令
## Django測試
cd web
python .\manage.py runserver

## Celery
cd web
python3 -m celery -A web worker [--detach] -l info -P eventlet(注意permission)

## 移除uwsgi
sudo pkill -f uwsgi -9