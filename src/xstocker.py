
import time
from predict_price import web_loader
from bson.objectid import ObjectId
from predict_price import db_manager
from tools.mongo import MongoManager
from predict_price import manager
from define import DB_KEY
import numpy
from tools import stocklist
mongo_mgr = MongoManager("mongodb://stock:stock@192.168.1.14:27017/stock")
from datetime import datetime
def get_basic_info(stock_id:str, date_time:str=None):
   # print("date time = " + str(date_time))
    if date_time is None or date_time.strip() == "":
    #    print("load newest")
        result = mongo_mgr.find_one("stock", "Outline", {DB_KEY.OBJECT_ID:ObjectId("5b940a041e6fe6eb0d8a53b2")})
        latest_day = result[DB_KEY.LATEST_DAY]
    else:
     #   print("load date time:" + date_time)
        latest_day = date_time.replace('/', '')

    r = mongo_mgr.find_one("stock", "DailyInfo_{}".format(latest_day[:6]), {'stkid':stock_id })
    daily_info = None
    name = None
    print("r[\"items\"]:  "  , str(r), "st ", stock_id , " latest_day[:6]", latest_day[:6])
    if r and latest_day in r["items"]:
        daily_info = r["items"][latest_day]
    if r:
        name = r["name"]
    print("name {}  daily_price: {}".format(name, daily_info))
    return {"name": name, "info":daily_info}

def load_list():
    twse = stocklist.StockListHolder.read_stock_ids(2)
    tpex = stocklist.StockListHolder.read_stock_ids(2)
    
    return numpy.append(twse, tpex).tolist()

def get_predict_price(stock_id:str):
    tbl = db_manager.fetch_predict_price(stock_id)[1]
    return tbl

def load_stock_info(stock_id:str):
    tbl = web_loader.load(stock_id)
    return tbl

def check_db_has_predict_price(stock_id:str, quarter:str=None):
    return db_manager.check_db_has_predict_price(stock_id, quarter)

def check_res_has_per_pbr_data(stock_id):
    return manager.has_per_pbr_file(stock_id)

def get_predict_price2(stock_id:str, quarter:str=None):
    df = manager.execute(stock_id, quarter, True)
    expensive =  df.iloc[0, [0]].values[0]
    resonable =  df.iloc[0, [1]].values[0]
    cheap =  df.iloc[0, [2]].values[0]
    return {
        DB_KEY.EXPENSIVE:expensive, 
        DB_KEY.RESONABLE:resonable, 
        DB_KEY.CHEAP:cheap}

if __name__ == '__main__':
    print (str(load_list()))