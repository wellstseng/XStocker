from resonable_price import resonable_price
import time
def get_stock_info(stock_id:str):
    tbl = {}
    
    
    df = resonable_price.execute(stock_id)
    if df is not None:
        tbl["expensive"] =  df.iloc[0, [0]].values[0]
        tbl["resonable"] =  df.iloc[0, [1]].values[0]
        tbl["cheap"] =  df.iloc[0, [2]].values[0]  
        time.sleep(1)
    return tbl