from lamp.utils.absattr import AbsAttrPassThrough
from lamp.log import log

class BaseView(AbsAttrPassThrough):
    @property
    def stock(self):
        return self._datasource.stock

    def get_last_n_days_info(self, n):
        ret = []
        for i in range(n-1, -1, -1):
            info = self.stock.get_last_n_day_info(i)
            ret.append(info)

        return ret

    def get_last_n_days_price(self, n):
        info = self.get_last_n_days_info(n)
        return [x['close'] for x in info]

    def get_last_n_days_date(self, n):
        # just mock dates
        return list(range(n))
        # info = self.get_last_n_days_info(n)
        # return [x['date'] for x in info]

    @property
    def last_n_days_date(self):
        ret = self.get_last_n_days_date(11)
        return ret

    @property
    def last_n_days_price(self):
        return self.get_last_n_days_price(11)
