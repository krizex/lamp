from lamp.model import Trend
from lamp.log import log
from lamp.utils.util import calc_ruler, parallel_apply, constructor_of
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
        self.stop_loss_rate = 0.1
        # down below MA40
        self.stop_benefit_down_rate = 0.03

    def weight_on_ruler(self, hold_cnt):
        ruler = [2, 3, 3, 2]
        if hold_cnt < len(ruler):
            return ruler[hold_cnt]
        else:
            return 1

    def next_buy_price(self):
        return self.start_price * ((1 + self.ratio) ** self.cur_hold)

    def next_buy_cnt(self):
        return self.weight_on_ruler(self.cur_hold) * self.unit

    def cur_flush_price(self):
        buy_price = self.next_buy_price() / (1 + self.ratio)
        return buy_price * (1 - self.stop_loss_rate)

    def cur_flush_cnt(self):
        if self.cur_hold <= 0:
            return 0
        else:
            return self.weight_on_ruler(self.cur_hold - 1) * self.unit

    def stop_benefit_price(self):
        return self.cur_price_ma40 * (1 - self.stop_benefit_down_rate)

    def calc_op_position_of_cur_price(self):
        low = self.cur_flush_price()
        high = self.next_buy_price()
        return (self.cur_price - low) / 1.0 / (high - low)

    def calc_cur_hold(self):
        if self.cur_hold <= 0:
            return 0
        else:
            total = 0.0
            for i in range(self.cur_hold):
                total += self.weight_on_ruler(i)
            return total / 10.0

    def break_highest(self):
        highest = self.stock.get_highest_in_past_n_days(self.trend_up_days_cnt)
        return self.cur_price >= highest



def get_trends():
    records = Trend.query.all()
    def build(x):
        return constructor_of(TrendUnit)(x)

    records = parallel_apply(records, build)
    records = sorted(records)

    return records
