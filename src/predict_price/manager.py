#%%
# -*- coding: utf-8 -*-

import re
import requests
from io import open
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys,os
import time
import platform
TEST_MODE = False

class PredicePriceDefine:
    LOCK = False
    CD_TIME = 10
    if platform.system() == "Linux":
        PER_PBR_FILE_PATH_FMT = "/home/www/XStocker/src/predict_price/res/PER_PBR_{}.html"
    else:
        PER_PBR_FILE_PATH_FMT = "D:/Github/XStocker/src/predict_price/res/PER_PBR_{}.html"

def has_per_pbr_file(stock_id):
    file_path = PredicePriceDefine.PER_PBR_FILE_PATH_FMT.format(stock_id)
    return os.path.isfile(file_path)

def pe_ratio_calculator(str_price:str, str_predict_eps:str):
    predict_eps = float(str_predict_eps) if '-' not in str_predict_eps else None
    price = float(str_price) if '-' not in str_price else None
    pe_ratio = None
    if price is not None and predict_eps is not None:
        pe_ratio = round(price / predict_eps, 2)
    return str(pe_ratio) if pe_ratio is not None else '-'

def predict_price(str_pe:str, str_predict_eps:str):
    predict_eps = float(str_predict_eps) if '-' not in str_predict_eps else None
    pe = float(str_pe) if '-' not in str_pe else None

    price =None
    if pe is not None and predict_eps is not None:
        price = round(predict_eps*pe,2)
    return str(price) if price is not None else '-'

def average_price(rows, base_amount):
    t = 0
    if len(rows) >= base_amount:
        for v in rows:
            if '-' not in str(v) and v is not np.nan and v is not None:
                t += float(v)
            else:
                t = None
                break
    else:
        t = None
    return str(round(t/4, 2)) if t is not None else '-'

def load_per_pbr_data(stock_id:str, cache:bool=False, need_sleep=False):
    headers = {'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded;',
        'origin': 'https://goodinfo.tw',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    headers['referer'] = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID={0}&YEAR_PERIOD=9999'.format(stock_id)
    r = requests.post('https://goodinfo.tw/StockInfo/StockBzPerformance.asp', data = {'STOCK_ID': stock_id,'YEAR_PERIOD': '9999','RPT_CAT': 'M_QUAR','STEP': 'DATA','SHEET': 'PER/PBR',}, headers = headers)
    r.encoding = 'utf8'
    result = r.text
    
    if cache == True:
        file_path = PredicePriceDefine.PER_PBR_FILE_PATH_FMT.format(stock_id)
        with open(file_path, 'a+', encoding='utf8') as f:
            f.write(result)
            f.close()
    return result

def get_dataframe(stock_id:str, cache:bool=False):
    if not stock_id:
        return None

    result = ""   
    if not has_per_pbr_file(stock_id):       
        result = load_per_pbr_data(stock_id, cache)
    else:
        print("load per/pbr from source", stock_id)
        file_path = PredicePriceDefine.PER_PBR_FILE_PATH_FMT.format(stock_id)
        with open(file_path, 'r', encoding='utf8') as f:
            result = f.readline()  
    soup = BeautifulSoup(result, 'html.parser')
    result_tbl = soup.find('table', attrs={'class':'solid_1_padding_4_0_tbl'})
    tr_rows = result_tbl.find_all('tr', id=re.compile(r'row'))

    tbl = []
    for row in tr_rows:
        td_values = row.find_all('td')
        values=[]
        for v in td_values:
            nobr = v.nobr
            if nobr.a is None:            
                values.append(nobr.contents[0])
            else:
                values.append(nobr.a.contents[0])
        tbl.append(values)
    df = pd.DataFrame(data=tbl,columns=['季度','股本','財報評分','最高價','最低價','收盤價','平均價','漲跌','漲跌比率','EPS','最高PER','最低PER','平均PER','BPS','最高PBR','最低PBR','平均PBR'])
    df.set_index('季度',inplace=True)
    #建立新欄位
    df = df.join(pd.DataFrame(columns=['預估EPS', '高價本益比','均價本益比','低價本益比','單季昂貴價','單季合理價','單季便宜價','四季昂貴均價','四季合理均價','四季便宜均價']))

    i = 0
    for _, row in df.iterrows():
        #計算近四季EPS
        four_eps = df.iloc[i:i+4, df.columns.get_loc('EPS')]
        predict_quarter_eps = 0
        if len(four_eps) >= 4:
            for v in four_eps:
                if '-' not in v:
                    predict_quarter_eps += float(v)
                else:
                    predict_quarter_eps = None
                    break
        else:
            predict_quarter_eps = None
        row['預估EPS'] = str(round(predict_quarter_eps, 2)) if predict_quarter_eps is not None else '-'


        #計算本益比
        row['高價本益比'] = pe_ratio_calculator(row['最高價'], row['預估EPS'])
        row['均價本益比'] = pe_ratio_calculator(row['平均價'], row['預估EPS'])
        row['低價本益比'] = pe_ratio_calculator(row['最低價'], row['預估EPS'])
        
        #計算單季預估價格
        row['單季昂貴價'] = predict_price(row['高價本益比'], row['預估EPS'])
        row['單季合理價'] = predict_price(row['均價本益比'], row['預估EPS'])
        row['單季便宜價'] = predict_price(row['低價本益比'], row['預估EPS'])  
        i+=1

    j = 0
    for _, row in df.iterrows():
        row['四季昂貴均價'] = average_price(df.iloc[j:j+4,df.columns.get_loc('單季昂貴價')],4)
        row['四季合理均價'] = average_price(df.iloc[j:j+4,df.columns.get_loc('單季合理價')],4)
        row['四季便宜均價'] = average_price(df.iloc[j:j+4,df.columns.get_loc('單季便宜價')],4)
        j+=1
    return df

def execute(stock_id, quarter:str=None, cache_data:bool=False):    
    df = get_dataframe(stock_id, cache_data)
    if df is None:
        print("dataframe is None")
        return None
    else:
        quarter = df.index[0] if not quarter else quarter
        if "Q" not in quarter:
            quarter = "{}Q{}".format(quarter[:4], quarter[-1])
        result = df.loc[[quarter], ['四季昂貴均價', '四季合理均價','四季便宜均價']]        
        return result
  

if __name__ == '__main__':
    stock_id = ""
    quarter = None
    cnt = len(sys.argv)
    if not TEST_MODE:
        if cnt >= 2:
            stock_id = str(sys.argv[1])
        if cnt >= 3:
            quarter =  str(sys.argv[2])
   
    result = execute(stock_id, quarter, True)
    print(result)
