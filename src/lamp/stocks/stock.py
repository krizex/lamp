import tushare as ts
from lamp.utils.util import ndays_before_today
from lamp.log import log


class Stock(object):
    def __init__(self, code):
        self.code = code
        self.df = self.get_k_data()
        try:
            self.name = StockMgr.get_stock_name(self.code)
        except Exception as e:
            # log.exception('Error when get stock name')
            self.name = 'UNKNOWN'

    def get_k_data(self):
        try:
            return ts.get_k_data(self.code, retry_count=10)
        except:
            cons = ts.get_apis()
            return ts.bar(self.code, conn=cons, retry_count=10)

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

    def get_highest_in_n_days(self, n):
        return self.df[-n:]['close'].max()

    def get_lowest_in_n_days(self, n):
        return self.df[-n:]['close'].min()


class __StockMgr(object):
    def __init__(self):
        self.inited = False
        self.df = None

    def _init(self):
        if not self.inited:
            self.df = self._init_basics()

    def _init_basics(self):
        if self.skip:
            return self.df

        for _ in range(1):
            try:
                log.info('Fetching stock basics...')
                pro = ts.pro_api('4105aca09e41fde2adac11ff8cdf7e05cef205d946e06935562e0010')
                ret = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
                # ret = ts.get_stock_basics()
                log.info('Fetched')
                self.inited = True
                return ret
            except:
                log.exception('Failed to get stock basics')

        self.skip = True
        return None

    def full_code(self, code):
        if code.startswith('60'):
            return code + '.SH'
        else:
            return code + '.SZ'

    def get_stock_info(self, code):
        self._init()

        code = self.full_code(code)

        return self.df.loc[self.df['ts_code'] == code].iloc[0]

    def get_stock_name(self, code):
        return self.get_stock_info(code)['name']


StockMgr = __StockMgr()

