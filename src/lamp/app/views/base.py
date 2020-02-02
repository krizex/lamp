from lamp.utils.absattr import AbsAttrPassThrough
from lamp.log import log
from lamp.app import conf


class BaseView(AbsAttrPassThrough):
    @property
    def stock(self):
        return self._datasource.stock

    @property
    def last_n_days_date(self):
        ret = self._datasource.get_last_n_days_date(conf.DETAIL_INFO_OF_LAST_DAYS)
        return ret

    @property
    def last_n_days_price(self):
        return self._datasource.get_last_n_days_price(conf.DETAIL_INFO_OF_LAST_DAYS)

    @property
    def last_n_days_vol(self):
        return self._datasource.get_last_n_days_vol(conf.DETAIL_INFO_OF_LAST_DAYS)
