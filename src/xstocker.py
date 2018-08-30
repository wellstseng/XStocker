
import time
#from predict_price import web_loader

from predict_price import db_manager
def get_stock_info(stock_id:str):
    #tbl = web_loader.load(stock_id)
    tbl = db_manager.fetch_predict_price(stock_id)[1]
    return tbl


