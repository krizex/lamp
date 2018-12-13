import tushare as ts
from lamp.utils.util import ndays_before_today
from lamp.log import log
from lamp import config
from lamp.basis import gen
from lamp.utils.file.sf import SharedFile
import json
import os


class Stock(object):
    def __init__(self, code):
        self.code = code
        self.df = self.get_k_data()
        self.is_fund = False
        try:
            self.name = StockMgr.get_stock_name(self.code)
        except Exception as e:
            # log.exception('Error when get stock name')
            self.name = 'UNKNOWN'
            self.is_fund = True

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
        self._init_basis()

    def _init_basis(self):
        f = config.basis_persistent_file
        sf = SharedFile(f)
        sf.exclusive_create(gen.fetch_basis)
        with sf.open_read() as f:
            self.json = json.load(f)

    def full_code(self, code):
        if code.startswith('60'):
            return code + '.SH'
        else:
            return code + '.SZ'

    def get_stock_info(self, code):
        code = self.full_code(code)
        return self.json[code]

    def get_stock_name(self, code):
        return self.get_stock_info(code)['name']


StockMgr = __StockMgr()

