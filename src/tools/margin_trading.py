#%%
# -*- encoding: utf-8 -*-
import sys, os
if __name__ == "__main__":
    sys.path.append(os.path.abspath('./src'))

import requests
import csv
import pandas as pd
import define
import time
import datetime
from datetime import timedelta, date, datetime
import global_func

class MarginTrading:
    def get_data(self, data_type:int, stock_id:str, date:str):
        '''
        載入信用交易資料
        回傳DataFrame
        '''
        #取得市場類型
        market = define.Define.get_market_type(stock_id)
        #未知市場不處理
        if market == define.MarketType.UNKNOWN:
            print('unknown stock id: {}'.format(stock_id))
            return define.MarketType.UNKNOWN,None
        #檢查是否需從網路下載資料表
        file_path = self.check_load_margin_data(market, date) if data_type == define.MarginTradingType.MARGIN else self.check_load_daytrading_data(market, date) 
        #產生data frame回傳
        df =pd.read_csv(file_path, encoding='utf-8', header=0, index_col=0)        
        return market, df        
    def get_daytrade(self, stock_id:str, date:str):
        market, margin_df = self.get_data(define.MarginTradingType.MARGIN, stock_id, date)
        _, daytrading_df = self.get_data(define.MarginTradingType.DAYTRADING, stock_id, date)
        if market == define.MarketType.UNKNOWN:
            return None
        if not stock_id in margin_df.index.values or not stock_id in daytrading_df.index.values:
            return (None, None, None)
        short_selling = int(margin_df.at[stock_id, '資券互抵' if market == define.MarketType.TWSE else '資券相抵(張)'])
        day_trading = int(int(daytrading_df.at[stock_id, '當日沖銷交易成交股數'].replace(',',''))/1000) #換算張
        return short_selling+day_trading, short_selling, day_trading
    def get_rgzratio(self, stock_id:str, date:str):
        try:
            #print(margin_data.at[stock_id, '資券相抵(張)'])
            market, df = self.get_data(define.MarginTradingType.MARGIN, stock_id, date)
            if market == define.MarketType.UNKNOWN:
                return (None, None, None)
            if not stock_id in df.index.values:
                return (None, None, None)
            securities = int(df.at[stock_id, '券今餘' if market == define.MarketType.TWSE else '券餘額'].replace(',',''))
            financing = int(df.at[stock_id, '資今餘' if market == define.MarketType.TWSE else '資餘額'].replace(',',''))
            if financing == 0:
                return (0,securities, financing)
            return round(securities/financing*100, 2), securities, financing
        except:
            return (None, None, None)
    def check_load_margin_data(self, market:str, date:str):        
        '''
        檢查下載信用交易資料
        '''
        if market == define.MarketType.UNKNOWN:
            print('unknown market')
            return None
        #檢查檔案是否存在，不存在先從網路上下載
        file_path = define.Define.get_margin_file_path(market, date)
        if not os.path.isfile(file_path):
#region 透過網路下載資料並儲存
            #TWSE市場下載           
            if market == define.MarketType.TWSE:
                #格式化日期
                fixed_date = date.replace('/', '')
                #取得網路下載的字串
                text = self.__load_text(define.Define.TWSE_MARGIN_URL_FMT.format(fixed_date), define.Define.TWSE_MARGIN_REQ_HEADERS) 
                #標準化分析，刪除多餘的文字               
                title_text = "\"股票代號\",\"股票名稱\",\"資買進\",\"資賣出\",\"資現償\",\"資前餘額\",\"資今餘\",\"資限額\",\"券買進\",\"券賣出\",\"券現償\",\"券前餘\",\"券今餘\",\"券限額\",\"資券互抵\",\"註記\",\n"
                text_arr = [i.translate({ord(' '): None}) 
                        for i in text.split('\n') 
                        if len(i.split('",')) == 17]    
                if len(text_arr) > 1:     
                    #寫入CSV檔案
                    del text_arr[0]
                    initialize_text = "\n".join(text_arr)
                    self.__save_text(file_path, title_text+initialize_text)
                    print('load twse margin done')
                else:
                    print("no twse margin data")
            else: #TPEX市場下載
                #轉換西元為民國
                roc_date = '/'.join([str(int(date.split('/')[0]) - 1911)] + date.split('/')[1:])
                #取得網路下載的字串
                text = self.__load_text(define.Define.TPEX_MARGIN_URL_FMT.format(roc_date), define.Define.TPEX_MARGIN_REQ_HEADERS)
                #標準化，移除多餘的文字                
                text_arr = [i.translate({ord(' '): None}) 
                                for i in text.split('\n') 
                                if len(i.split('",')) == 20 or len(i.split('",')) == 21 or ("代號" in i and "名稱" in i)]
                if len(text_arr) > 1:
                    #寫入CSV檔案
                    initialize_text = "\n".join(text_arr)
                    self.__save_text(file_path, initialize_text)
                    print('load tpex margin done')
                else:
                    print('no tpex margin data')
#endregion
        return file_path
    def check_load_daytrading_data(self, market:str, date:str):
        '''
        檢查下載現股當沖資料
        '''
        if market == define.MarketType.UNKNOWN:
            print('unknown market')
            return None
        file_path = define.Define.get_daytrading_file_path(market, date)
        self.__check_make_dir(file_path)
        text_arr = None
        initialize_text = ""
        #檢查是否需重新下載
        if not os.path.isfile(file_path):
            #TWSE市場下載           
            if market == define.MarketType.TWSE:            
                #格式化日期
                fixed_date = date.replace('/', '')
                #取得網路下載的字串
                text = self.__load_text(define.Define.TWSE_DAYTRADING_URL_FMT.format(fixed_date), define.Define.TWSE_DAYTRADING_REQ_HEADERS) 
                #標準化分析，刪除多餘的文字  
                text_arr = [i.translate({ord(' '): None}) 
                            for i in text.split('\n') 
                                if len(i.split('",')) == 7]
                if len(text_arr) > 1:
                    #移除前2行多餘的字串
                    del text_arr[0]
                    del text_arr[0]                            
                    initialize_text = "\n".join(text_arr)                            
                       
                    #寫入CSV檔案
                    self.__save_text(file_path, initialize_text)
                    print('load twse daytrading done')
                else:
                    print('no  twse daytrading data')
            else: #TPEX市場下載
                #轉換西元為民國
                roc_date = '/'.join([str(int(date.split('/')[0]) - 1911)] + date.split('/')[1:])
                #取得網路下載的字串
                text = self.__load_text(define.Define.TPEX_DAYTRADING_URL_FMT.format(roc_date), define.Define.TPEX_DAYTRADING_REQ_HEADERS)
               
                #標準化，移除多餘的文字   
                text_arr = [i.translate({ord(' '): None}) 
                            for i in text.split('\n') 
                            if len(i.split('",')) == 6 ]
                if len(text_arr) > 1:    
                    del text_arr[0]
                    title_text = '"證券代號","證券名稱","暫停現股賣出後現款買進當沖註記","當日沖銷交易成交股數","當日沖銷交易買進成交金額","當日沖銷交易賣出成交金額"\n'
                    initialize_text = "\n".join(text_arr)
                    #寫入CSV檔案
                    self.__save_text(file_path, title_text+initialize_text)
                    
                    print('load tpex daytradingv done')
                else:
                    print('no tpex daytrading data')
        return file_path

    def __check_make_dir(self, file_path:str):
        dir_name = os.path.dirname(file_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
    def __load_text(self, url:str, headers:dict):
        '''
        使用request下載CSV字串
        '''       
        time.sleep(3)
        r = requests.post(url, headers = headers)
        r.encoding = 'big5'        
        return r.text
    
    def __save_text(self, file_path:str, text:str):
        '''
        存檔
        '''
        self.__check_make_dir(file_path)
        with open(file_path, "w", encoding='utf8', newline='') as f:
            f.write(text)
            f.close()

def update_range( data_type, market_type, start_date=None, end_date=None):    
    if start_date == None:
        start_date = datetime.now().strftime("%Y/%m/%d")

    if end_date == None:     
        end_date = global_func.get_latest_file_date(define.Define.SRC_DATA_PATH_FMT.format(data_type, market_type))   

    s = start_date.split('/')
    e = end_date.split('/')
    start_date = date(int(s[0]), int(s[1]), int(s[2]))
    end_date = date(int(e[0]), int(e[1]), int(e[2]))
    t = MarginTrading()
    if start_date != None and end_date != None:
        print("update {0}[{1}] from date {2} to  {3}".format(data_type, market_type, start_date, end_date))
        
        for single_date in global_func.daterange(start_date, end_date):
            src_date = single_date.strftime("%Y/%m/%d")
            print('load csv   date:{}'.format(src_date))
            if data_type == define.DataType.DAY_TRADIN:
                t.check_load_daytrading_data(market_type, src_date)
            elif data_type == define.DataType.MARGIN:
                t.check_load_margin_data(market_type, src_date)
            else:
                raise Exception("Invalid Margin Type:{0}".format(data_type))
            print("sleep 10")
            time.sleep(10)
        print('done')

   


if __name__=="__main__":
    update_range("margin", "twse")
    update_range("margin", "tpex")
    update_range("day_trading", "twse")
    update_range("day_trading", "tpex")