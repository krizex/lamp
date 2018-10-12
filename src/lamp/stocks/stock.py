import tushare as ts
from lamp.utils.util import ndays_before_today


class Stock(object):
    def __init__(self, code):
        self.code = code
        self.df = self.get_k_data(ndays_before_today(30).strftime('%Y-%m-%d'), '')
        self.name = StockMgr.get_stock_name(self.code)

    def get_k_data(self, start, end):
        return ts.get_k_data(self.code, start, end, retry_count=10)

    def get_last_day_info(self):
        today = self.df.shape[0] - 1
        return self.df.iloc[today]

    def get_last_day_close(self):
        return self.get_last_day_info()['close']


class __StockMgr(object):
    def __init__(self):
        self.df = ts.get_stock_basics()

    def get_stock_info(self, code):
        return self.df.ix[code]

    def get_stock_name(self, code):
        return self.get_stock_info(code)['name'].decode('utf-8')


StockMgr = __StockMgr()

