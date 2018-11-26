from lamp.stocks.stock import Stock, StockMgr
from lamp.model import Candidate, Grid
from lamp.log import log
from lamp.utils.util import calc_ruler
from abc import ABCMeta, abstractproperty, abstractmethod
import traceback


class GridUnit(object):
    def __init__(self, grid):
        self.code = grid.code
        self.name = grid.name
        self.size = grid.size
        self.unit = grid.unit
        self.note = grid.note
        self.ruler, self.width = calc_ruler(grid.high, grid.low, grid.size)
        self.fill_info()

    def fill_info(self):
        log.debug('Fetching %s', self.code)
        self.stock = Stock(self.code)
        # self.cur_price = 0.1
        # self.cur_p_change = 0.0
        try:
            if not self.name:
                self.name = self.stock.name
            self.cur_price = self.stock.get_last_day_close()
            self.cur_p_change = self.stock.get_last_day_p_change()
        except Exception as e:
            log.exception('Cannot get info for %s' % self.code)

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
        rets = []
        for hold in self.calc_hold_cnt():
            if hold <= 0 or hold >= self.size:
                rets.append(-1)
            else:
                sell = self.ruler[hold - 1]
                buy = self.ruler[hold + 1]
                d = 1 - (self.cur_price - buy) / 1.0 / (sell - buy)
                rets.append(d)
        return rets

    def trend_start_ndays(self, n):
        return self.stock.get_highest_in_n_days(n)

    def trend_stop_ndays(self, n):
        return self.stock.get_lowest_in_n_days(n)


def get_grids():
    StockMgr.skip = False
    records = Grid.query.all()
    records = [GridUnit(rec) for rec in records]

    return records
