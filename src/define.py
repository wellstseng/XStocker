import os
import twstock
class Define:
    FILE_PATH = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
    LIST_PATH_FMT = FILE_PATH + '/data/list{}.csv'
    TEST_HTML_PATH = FILE_PATH + '/data/test/stock_list.txt'
    TEST_LEADER_TRADE_PATH = FILE_PATH + '/res/test/leader_trade.txt'
    SECRET_PATH = FILE_PATH + '/auth/client_secret.json'
    XLS_PATH = FILE_PATH + '/res/StockGradingSystem.xlsx'
    MARGIN_PATH_FMT = FILE_PATH + '/data/margin/{0}/{1}.csv'
    DAYTRADING_PATH_FMT = FILE_PATH + '/data/day_trading/{1}/{0}.csv'
    DAILY_PRICE_FMT = FILE_PATH + "/data/price/{0}/{1}.csv"
    BRANCH_LIST = FILE_PATH + '/res/branchList.csv'
    LEGAL_PERSON_PATH_FMT = FILE_PATH + '/res/legalperson/{0}_M{1}.csv'
    SRC_DATA_PATH_FMT = FILE_PATH + "/data/{0}/{1}"
    TWSE_MARGIN_URL_FMT = 'http://www.tse.com.tw/exchangeReport/MI_MARGN?response=csv&date={0}&selectType=ALL'
    TWSE_MARGIN_REQ_HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",        
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection":"keep-alive",
        "Host":"www.tse.com.tw",
        "Upgrade-Insecure-Requests":"1"
    }
    
    TPEX_MARGIN_URL_FMT = 'http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=csv&d={0}&s=0,asc'
    TPEX_MARGIN_REQ_HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection":"keep-alive",
        "Cookie":"_ga=GA1.3.2117065285.1533458331; _gid=GA1.3.751473853.1534577751",
        "Host":"www.tpex.org.tw",
        "Upgrade-Insecure-Requests":"1",
        "Referer": "http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal.php?l=zh-tw"
    }
    TWSE_DAYTRADING_URL_FMT = 'http://www.tse.com.tw/exchangeReport/TWTB4U?response=csv&date={0}&selectType=All'
    TWSE_DAYTRADING_REQ_HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Referer":"http://www.tse.com.tw/zh/page/trading/exchange/TWTB4U.html",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection":"keep-alive",
        "Cookie":"_ga=GA1.3.2036274003.1532407181; _gid=GA1.3.1849235811.1532407181; JSESSIONID=9994EBB73146154704AC81F3F5770114; _gat=1",
        "Host":"www.tse.com.tw",
        "Upgrade-Insecure-Requests":"1"
    }
    TPEX_DAYTRADING_URL_FMT = 'http://www.tpex.org.tw/web/stock/trading/intraday_stat/intraday_trading_stat_result.php?l=zh-tw&d={0}&s=0,asc,0&o=csv'
    TPEX_DAYTRADING_REQ_HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection":"keep-alive",
        "Cookie":"_ga=GA1.3.1880665680.1532410072; _gid=GA1.3.1462450588.1532519038",
        "Host":"www.tpex.org.tw",
        "Upgrade-Insecure-Requests":"1",
		"Referer": "http://www.tpex.org.tw/web/stock/trading/intraday_stat/intraday_trading_stat.php?l=zh-tw"
    }
    
    TWSE_DAILY_PRICE_URL_FMT = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={}&type=ALL'
    TWSE_DAILY_PRICE_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=F9F448B023345534D12186AA912F365B; _ga=GA1.3.2036274003.1532407181; _gid=GA1.3.1849235811.1532407181; _gat=1",
        "Host":"www.twse.com.tw",
        "Referer": "http://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    TPEX_DAILY_PRICE_URL_FMT = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d={0}&s=0,asc,0" 
    TPEX_DAILY_PRICE_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.3.1880665680.1532410072; _gid=GA1.3.328060233.1532410072; _gat=1",
        "Host":"www.tpex.org.tw",
        "Referer": "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote.php?l=zh-tw",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    TWSE_LEGAL_PERSON_TRADE_FMT = 'http://www.twse.com.tw/fund/T86?response=csv&date={}&selectType=ALL'
    TPEX_LEGAL_PERSON_TRADE_FMT ='http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=csv&se=EW&t=D&d={}&s=0,asc'
    STOCK_LIST_SHEET_NAME = 'ID'
    
    @staticmethod
    def get_list_path(data_type):
        return Define.LIST_PATH_FMT.format(data_type)
    
    @staticmethod
    def get_margin_file_path(market, date):
        date = date.replace('/', '')
        return Define.MARGIN_PATH_FMT.format(market, date)
    
    @staticmethod
    def get_daytrading_file_path(market, date):
        date = date.replace('/', '')
        return Define.DAYTRADING_PATH_FMT.format(date, market)

    @staticmethod
    def get_market_type(stock_id: str):
        if stock_id in twstock.twse and not stock_id in twstock.tpex:
            return MarketType.TWSE
        elif not stock_id in twstock.twse and stock_id in twstock.tpex:
            return MarketType.TPEX
        else:
            return MarketType.UNKNOWN

    @staticmethod
    def get_legal_person_file_path(market, date):
        date = date.replace('/', '')
        return Define.LEGAL_PERSON_PATH_FMT.format(date, market)

class MarketType:
    UNKNOWN = 'unknown'
    TWSE = 'twse'
    TPEX = 'tpex'

    @staticmethod
    def get_names():
        return (MarketType.TWSE, MarketType.TPEX)

class MarginTradingType:
    MARGIN = 0
    DAYTRADING = 1

class DataType:
    MARGIN = "margin"
    DAY_TRADIN = "day_trading"
    PRICE = "price"

    @staticmethod
    def get_names():
        return (DataType.MARGIN, DataType.DAY_TRADIN)

class DB_KEY:
    STOCK_ID="stkid"
    DATE="date"
    OPEN="open"
    CLOSE="close"
    HIGH="high"
    LOW="low"
    VOLUME="vol"
    TURNOVER="to"
    TRANSACTION="tr"
    NAME="name"

    LOG_DATE="logd"
    PARSE_LOG="parse"
    PURCHASE_BUY="pbuy"
    PURCHASE_SELL="psell"
    PURCHASE_REPAYMENT="pr"
    PURCHASE_BEFORE_REMAIN="pbr"
    PURCHASE_TODAY_REMAIN="ptr"
    PURCHASE_LIMIT="pl"
    SELL_BUY="sb"
    SELL_SELL="ss"
    SELL_REPAYMENT="sr"
    SELL_BEFORE_REMAIN="sbr"
    SELL_TODAY_REMAIN="str"
    SELL_LIMIT="sl"
    MARGIN_OFFSET="mo"

    EXPENSIVE = "expen"
    RESONABLE = "reson"
    CHEAP = "cheap"
    LATEST_QUARTER = "lqua"
    LATEST_DAY = "latsd"
    OBJECT_ID="_id"

if __name__ == "__main__" :
    print(Define.FILE_PATH)