from lamp.utils.absattr import AbsAttrPassThrough
from lamp.log import log


class BaseView(AbsAttrPassThrough):
    @property
    def stock(self):
        return self._datasource.stock

    @property
    def last_n_days_date(self):
        ret = self._datasource.get_last_n_days_date(22)
        return ret

    @property
    def last_n_days_price(self):
        return self._datasource.get_last_n_days_price(22)
