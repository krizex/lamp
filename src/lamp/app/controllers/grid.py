from lamp.stocks.stock import Stock, StockMgr
from lamp.stocks.fund import Fund
from lamp.model import Candidate, Grid
from lamp.log import log
from lamp.utils.util import calc_ruler, parallel_apply
from abc import ABCMeta, abstractproperty, abstractmethod
import traceback


class GridUnit(object):
    def __init__(self, grid):
        self.code = grid.code
        self.name = grid.name
        self.size = grid.size
        self.unit = grid.unit
        self.note = grid.note
        self.own = grid.own
        self.ruler, self.width = calc_ruler(grid.high, grid.low, grid.size)
        self.fill_stock_info()
        self.is_fund = False
        # TODO: fix the value assesment
        # self.is_fund = self.stock.is_fund
        if self.is_fund:
            self.fill_fund_info()

    def fill_stock_info(self):
        log.debug('Fetching %s', self.code)
        self.stock = Stock(self.code)
        try:
            if not self.name:
                self.name = self.stock.name
            self.cur_price = self.stock.get_last_day_close()
            self.cur_p_change = self.stock.get_last_day_p_change()
        except Exception as e:
            log.exception('Cannot get info for %s' % self.code)

    def fill_fund_info(self):
        self.fund = Fund(self.code)

    def calc_cur_ruler_pos(self):
        """The first sell pos"""
        for i, price in enumerate(self.ruler):
            if self.cur_price >= price:
                return i - 1

        return len(self.ruler) - 1

    def calc_hold_cnt(self):
        cur_pos = self.calc_cur_ruler_pos()
        if cur_pos < 0:
            return [0, 0]
        elif cur_pos >= len(self.ruler) - 1:
            # full hold
            return [self.size, self.size]
        else:
            return [cur_pos, cur_pos + 1]

    def calc_next_op_distance(self):
        def calc_pos(sell, buy):
            return 1 - (self.cur_price - buy) / 1.0 / (sell - buy)

        rets = []
        for hold in self.calc_hold_cnt():
            if hold <= 0:
                if self.cur_price > self.ruler[0]:
                    rets.append(-1)
                else:
                    virt_sell = self.ruler[0]
                    buy = self.ruler[1]
                    d = calc_pos(virt_sell, buy)
                    rets.append(d)
            elif hold >= self.size:
                if self.cur_price < self.ruler[-1]:
                    rets.append(-1)
                else:
                    sell = self.ruler[-2]
                    virt_buy = self.ruler[-1]
                    d = calc_pos(sell, virt_buy)
                    rets.append(d)
            else:
                sell = self.ruler[hold - 1]
                buy = self.ruler[hold + 1]
                d = calc_pos(sell, buy)
                rets.append(d)
        return rets

    def trend_start_ndays(self, n):
        return self.stock.get_highest_in_n_days(n)

    def trend_stop_ndays(self, n):
        return self.stock.get_lowest_in_n_days(n)

    def calc_premium(self):
        cur_val = self.cur_price
        ass_val = self.fund.ass_val
        return (cur_val - ass_val) / 1.0 / ass_val

    def __cmp__(self, other):
        if self.own > other.own:
            return -1
        elif self.own < other.own:
            return 1
        else:
            return 0


def get_grids():
    records = Grid.query.all()
    def build(x):
        return GridUnit(x)

    records = parallel_apply(records, build)
    records = sorted(records)

    return records
