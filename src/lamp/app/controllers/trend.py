from lamp.model import Trend
from lamp.log import log
from lamp.utils.util import calc_ruler, parallel_apply
from lamp.app.controllers.base import ObjectBaseUnit
from abc import ABCMeta, abstractproperty, abstractmethod
import traceback


class TrendUnit(ObjectBaseUnit):
    def __init__(self, trend):
        super(TrendUnit, self).__init__(trend.code, trend.name, trend.own)
        self.unit = trend.unit
        self.note = trend.note
        self.ratio = trend.ratio
        self.start_price = trend.start_price
        self.cur_hold = trend.cur_hold
        self.trend_up_days_cnt = 22
        self.trend_down_days_cnt = 11

    def next_buy(self):
        return self.start_price * ((1 + self.ratio) ** self.cur_hold)

    def flush_price(self):
        highest = self.trend_high_ndays(self.trend_up_days_cnt)
        return highest * 1.0 * ((1 - self.ratio) ** 2)

    def __cmp__(self, other):
        if self.own > other.own:
            return -1
        elif self.own < other.own:
            return 1
        else:
            return cmp(self.code, other.code)


def get_trends():
    records = Trend.query.all()
    def build(x):
        return TrendUnit(x)

    records = parallel_apply(records, build)
    records = sorted(records)

    return records
