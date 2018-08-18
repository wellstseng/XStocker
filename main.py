import sys
import src.tools.daily_price  as daily_price
from  src.define import Define as Define
from  src.define import MarketType as MarketType
import src.global_func
import src.importer.margin_trading_importer as data_importer
if sys.argv[1] == MarketType.TWSE:
    data_importer.import_to_mongo(sys.argv[1],sys.argv[2], sys.argv[3])
    #daily_price.load_range(MarketType.TWSE, Define.TWSE_DAILY_PRICE_URL_FMT, Define.TWSE_DAILY_PRICE_HEADERS, sys.argv[2], sys.argv[3], True, False)
elif sys.argv[1] == MarketType.TPEX:
    data_importer.import_to_mongo(sys.argv[1],sys.argv[2], sys.argv[3])
    #daily_price.load_range(MarketType.TPEX, Define.TPEX_DAILY_PRICE_URL_FMT, Define.TPEX_DAILY_PRICE_HEADERS, sys.argv[2], sys.argv[3], True, False)
else:
    print("Unknow market type, bye.")