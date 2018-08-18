#%%
# -*- encoding:utf-8 -*-
import sys, os

import requests
import io
import os.path
import time
from datetime import timedelta, date, datetime
import pandas as pd
import csv

try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import global_func
    import define
    from mongo import MongoManager
    from define import DB_KEY as DB_KEY
except:
    import src.global_func
    import src.define
    from src.tools.mongo import MongoManager
    from src.define import DB_KEY as DB_KEY
dfs={}
querys={} #{stockid:{'$set':{...}},...}
mongo_mgr = MongoManager("mongodb://stock:stock@192.168.1.14:27017/stock")
LOG_ENABLE = True
def normalize_file(market_type:str, file_path:str):
    with open(file_path, "r+", encoding='utf8') as f:
        text = f.read()
        text_arr = [i.translate({ord(' '): None, ord('='):None}).rstrip(',') 
            for i in text.split('\n') 
                if (len(i.split('",')) >= 15 and len(i.split('",')) <= 17) or "代號" in i]
        if market_type == define.MarketType.TPEX:
            if len(text_arr) > 0:             
                if "代號" in text_arr[0]:
                    del text_arr[0] 
                if len(text_arr) > 0:
                    length = len(text_arr[0].split('",')) if text_arr != None and len(text_arr) > 0 else 0
                    if "證券代號" not in text_arr[0]:
                        if length == 15:
                            text_arr.insert(0, "證券代號,證券名稱,收盤價,漲跌,開盤價,最高價,最低價,成交股數,成交金額,成交筆數,最後買價,最後賣價,發行股數,次日漲停價,次日跌停價")
                        elif length == 17:
                            text_arr.insert(0, "證券代號,證券名稱,收盤價,漲跌,開盤價,最高價,最低價,均價,成交股數,成交金額,成交筆數,最後買價,最後賣價,發行股數,次日參考價,次日漲停價,次日跌停價")
        else:
            if "證券代號" not in text_arr[0]:
                del text_arr[0] 
                    
        initialize_text = "\n".join(text_arr) 
        f.seek(0)
        f.truncate()
        f.write(initialize_text)
        f.close()
        # now_time = datetime.now()
        # mongo_mgr.upsert("stock", "Logger", {DB_KEY.LOG_DATE:now_time.strftime("%Y%m%d")}, 
        #     {"$push":{DB_KEY.PARSE_LOG:"{0}: {1}".format(now_time.strftime("%Y%m%d-%H:%M:%S"), "normalize file:{0} finish".format(file_path))}})
    if len(text_arr) <= 1:
        os.remove(file_path)

def load_df_files(market_type, start_date, end_date):
    print("load df files..........")
    cnt = 0
    for single_date in global_func.daterange(start_date, end_date):   
        print("\r", end="")     
        file_path = global_func.get_abs_path(define.Define.DAILY_PRICE_FMT.format(market_type, single_date.strftime("%Y%m%d")))
       
        if not os.path.isfile(file_path):
            continue
        normalize_file(market_type, file_path)  
        if not os.path.isfile(file_path):
            continue      
        df = pd.read_csv(file_path, header=0, dtype={"證券代號":str} )   
        df.set_index('證券代號', inplace=True)
        file_date = os.path.basename(file_path).split('.')[0]
        dfs[file_date] = df
        cnt +=1
        if LOG_ENABLE:
            sys.stdout.flush()     
            print("{0:10} {1:8}".format(file_date, cnt),end='')

def build_query():
    print("\nstart build query......")
    all_dfs=0
    for file_date, df in dfs.items():
        cnt = 0
        total = len(df.index)
        year_month = file_date[:6]
        if year_month not in querys:
            querys[year_month] = {}
        for index, series in df.iterrows():
            try:    
                
                print("\r", end="")
                series = df.loc[index]
                suspend = "--" in str(series["開盤價"])
                o = float(str(series["開盤價"]).replace(',','')) if not suspend else -1
                h = float(str(series["最高價"]).replace(',','')) if not suspend else -1
                l = float(str(series["最低價"]).replace(',','')) if not suspend else -1
                c = float(str(series["收盤價"]).replace(',','')) if not suspend else -1
                
                name =  series["證券名稱"]
                volume = int(round(int(series["成交股數"].replace(',',''))*0.001, 0)) if not suspend else 0
                turnover = round(int(series["成交金額"].replace(',',''))*0.00000001, 3)  if not suspend else 0
                transaction = int(series["成交筆數"].replace(',',''))  if not suspend else 0

                if index not in querys[year_month]:
                    querys[year_month][index] = {"$set":{DB_KEY.NAME:name}}

                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.OPEN)]=o
                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.HIGH)]=h
                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.LOW)]=l
                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.CLOSE)]=c
                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.VOLUME)]=volume
                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.TURNOVER)]=turnover
                querys[year_month][index]["$set"]["items.{0}.{1}".format(file_date, DB_KEY.TRANSACTION)]=transaction
                
                cnt += 1
                if LOG_ENABLE:
                    sys.stdout.flush()     
                    print("{0:10} {1:8} => {2:6}/{3:6}    {4:5}".format(file_date, index, cnt, total,all_dfs ),end='')
                
            except Exception as e:
                print("fail date:{} \n msg:{} \n data:{}".format(file_date, e, series))
                mongo_mgr.upsert("stock", "Logger", {DB_KEY.LOG_DATE:datetime.now().strftime("%Y%m%d")}, 
                    {"$push":{DB_KEY.PARSE_LOG:"build query fail date:{} \n msg:{} \n data:{}".format(file_date, e, series)}})
                break
        all_dfs+=1
        print("      Done")


def execute_query():
    print("execute querys .........")
    date_total = len(querys)
    date_cnt = 0
    for year_month, all_querys in  querys.items():    
        print("\n")    
        total = len(all_querys)    
        cnt=0
        for id, query in all_querys.items():            
            print("\r", end="")
            result = mongo_mgr.upsert("stock", "DailyInfo_{}".format(year_month), {DB_KEY.STOCK_ID:id}, query)
            if result['ok'] != 1.0:
                mongo_mgr.upsert("stock", "Logger", {DB_KEY.LOG_DATE:datetime.now().strftime("%Y%m%d")}, 
                        {"$push":{DB_KEY.PARSE_LOG:"mongo db upsert fail date:{0}, stock_id:{1}, query:{2}".format(file_date, index, query)}})
                raise Exception("mongo db upsert fail date:{0}, stock_id:{1}, query:{2}".format(file_date, index, query) )
            
            cnt += 1
            if LOG_ENABLE:
                sys.stdout.flush()     
                print("{0:10} => {1:6}/{2:6}".format(id, cnt, total ),end='')
        date_cnt+=1
      
    print("\n")

def import_to_mongo(market_type, start_date:str=None, end_date:str=None):
    if start_date == None:
        start_date = datetime.now().strftime("%Y/%m/%d")
    if end_date == None:
        end_date = global_func.get_latest_file_date(define.Define.SRC_DATA_PATH_FMT.format(define.DataType.PRICE,market_type))
 
    print("start:{0}  end:{1}".format(start_date, end_date))
    s = start_date.split("/")
    e= end_date.split("/")
    start_date = date(int(s[0]), int(s[1]), int(s[2]))
    end_date = date(int(e[0]), int(e[1]), int(e[2]))
    
    
    load_df_files(market_type, start_date, end_date)  
    build_query()
    execute_query()
    print("All Done")
    
