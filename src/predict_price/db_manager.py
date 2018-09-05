import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import manager
except:
    from predict_price import manager
import time
from datetime import timedelta, date, datetime

from define import DB_KEY
from tools.mongo import MongoManager
import logging
logger = logging.getLogger('django')

mongo_mgr = MongoManager("mongodb://stock:stock@192.168.1.14:27017/stock")

def add_log(log_string:str):
    now_time = datetime.now()
    mongo_mgr.upsert("stock", "Logger", {DB_KEY.LOG_DATE:now_time.strftime("%Y%m%d")}, 
        {"$push":{DB_KEY.PARSE_LOG:"{0}: {1}".format(now_time.strftime("%Y%m%d-%H:%M:%S"), log_string)}})

def __upsert_data(stock_id, quarter, latest_quarter=None):
    price_tbl = None
    if quarter is not None:
        quarter = quarter.replace("Q", "")
    df = manager.execute(stock_id, quarter)
    if df is not None:
        quarter = df.index[0].replace("Q","")
        expensive =  df.iloc[0, [0]].values[0]
        resonable =  df.iloc[0, [1]].values[0]
        cheap =  df.iloc[0, [2]].values[0]
        
        newest_quarter = latest_quarter if latest_quarter is not None else quarter
        if latest_quarter is not None:
            if int(quarter) > int(latest_quarter):
                 newest_quarter = quarter

        query = {
            "$set" : {
                DB_KEY.STOCK_ID:stock_id,
                DB_KEY.LATEST_QUARTER:newest_quarter,
                "datas.{0}.{1}".format(quarter, DB_KEY.EXPENSIVE):expensive,
                "datas.{0}.{1}".format(quarter, DB_KEY.RESONABLE):resonable,
                "datas.{0}.{1}".format(quarter, DB_KEY.CHEAP):cheap,
            }
        }
        result = mongo_mgr.upsert("stock", "predict_price", {DB_KEY.STOCK_ID:stock_id}, query)
        if result['ok'] != 1.0:
            print("Insert stock id:{0} resonable price fail:{1}".format(stock_id, str(result)))
        price_tbl=[expensive, resonable, cheap]
    return quarter, price_tbl

def fetch_predict_price(stock_id:str, quarter:str=None):
    if quarter is not None:
        quarter = quarter.replace("Q", "")
    price_tbl = None
    result = mongo_mgr.find_one("stock", "predict_price", {'stkid':stock_id})
    if result is None :
        logger.info("{0} is None fetch from www and insert to mongo")
        quarter, price_tbl = __upsert_data(stock_id, quarter)
    else:
        if quarter is None:
            quarter = result[DB_KEY.LATEST_QUARTER]
        if quarter not in result["datas"]:
            quarter, price_tbl = __upsert_data(stock_id, quarter)
        else:
            price_tbl = result["datas"][quarter]
            
    return quarter, price_tbl   

def check_db_has_predict_price(stock_id:str, quarter:str = None):
    result = mongo_mgr.find_one("stock", "predict_price", {'stkid':stock_id, })
    if result is None:
        return False
    else:
        if quarter is None:
            quarter = result[DB_KEY.LATEST_QUARTER]
        if quarter not in result["datas"]:
            return False
    return True

if __name__ == "__main__":
    print(fetch_predict_price("3546"))