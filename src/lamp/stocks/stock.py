import tushare as ts
from lamp.utils.util import ndays_before_today
from lamp.log import log


class Stock(object):
    def __init__(self, code):
        self.code = code
        self.df = self.get_k_data()
        self.name = StockMgr.get_stock_name(self.code)

    def get_k_data(self):
        return ts.get_k_data(self.code, retry_count=10)

    def get_last_n_day_info(self, n):
        day = self.df.shape[0] - 1 - n
        return self.df.iloc[day]

    def get_last_day_p_change(self):
        today = self.get_last_n_day_info(0)
        yesterday = self.get_last_n_day_info(1)
        return today['close'] / yesterday['close'] - 1.0

    def get_last_day_close(self):
        return self.get_last_n_day_info(0)['close']

    def get_last_day_date(self):
        return self.get_last_n_day_info(0)['date']


class __StockMgr(object):
    def __init__(self):
        self.inited = False
        self.df = None

    def _init(self):
        if not self.inited:
            self.df = self._init_basics()
            self.inited = True

    def _init_basics(self):
        for _ in range(10):
            try:
                log.info('Fetching stock basics...')
                ret = ts.get_stock_basics()
                log.info('Fetched')
                return ret
            except:
                log.exception('Failed to get stock basics')

    def get_stock_info(self, code):
        self._init()
        return self.df.ix[code]

    def get_stock_name(self, code):
        return self.get_stock_info(code)['name'].decode('utf-8')


StockMgr = __StockMgr()

