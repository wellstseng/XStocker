
import time
from predict_price import web_loader

from predict_price import db_manager
from tools.mongo import MongoManager

mongo_mgr = MongoManager("mongodb://stock:stock@192.168.1.14:27017/stock")

def get_basic_info(stock_id:str):
    r = mongo_mgr.find_one("stock", "DailyInfo_201808", {'stkid':stock_id })
    return str(r['items']) # 找最後一天

def get_predict_price(stock_id:str):
    tbl = db_manager.fetch_predict_price(stock_id)[1]
    return tbl

def load_stock_info(stock_id:str):
    tbl = web_loader.load(stock_id)
    return tbl

def check_db_has_predict_price(stock_id:str, quarter:str=None):
    return db_manager.check_db_has_predict_price(stock_id, quarter)