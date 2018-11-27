from lamp.stocks.stock import Stock, StockMgr
from lamp.log import log
from lamp.model import Candidate
import traceback



class CandidateUnit(object):
    def __init__(self, candidate):
        self.code = candidate.code
        self.name = candidate.name
        self.start_pe = candidate.start_pe
        self.stop_pe = candidate.stop_pe
        self.start_price = candidate.start_price
        self.own = candidate.own
        self.note = candidate.note
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

    @property
    def stop_price(self):
        return self.start_price * (1 + self.volatility_up)

    @property
    def stop_loss_price(self):
        return self.start_price / (1 + self.volatility_up)

    @property
    def volatility_up(self):
        return self.stop_pe / self.start_pe - 1

    @property
    def volatility_down(self):
        return (self.start_price - self.stop_loss_price) / self.start_price

    @property
    def quite_distance(self):
        """ hover around the target price, if not exit when beyonds the price, will return a negative value to make the order higher
        """
        if self.cur_price >= self.start_price:
            return (self.stop_price - self.cur_price) / self.cur_price
        else:
            return (self.cur_price - self.stop_loss_price) / self.cur_price

    @property
    def enter_distance(self):
        if self.cur_price >= self.start_price:
            return -(self.cur_price - self.start_price) / self.cur_price
        else:
            return (self.start_price - self.cur_price) / self.cur_price

    @property
    def cur_benefit(self):
        return (self.cur_price - self.start_price) / self.start_price

    def __cmp__(self, other):
        if self.own > other.own:
            return -1
        elif self.own < other.own:
            return 1
        # now self and other .own equals
        elif self.own == 1:
            # TODO reconsider the order
            return cmp(self.quite_distance, other.quite_distance)
        elif self.own == 0:
            return cmp(abs(self.enter_distance), abs(other.enter_distance))
        else:
            return cmp(self.cur_benefit, other.cur_benefit)

    def trend_start_ndays(self, n):
        return self.stock.get_highest_in_n_days(n)

    def trend_stop_ndays(self, n):
        return self.stock.get_lowest_in_n_days(n)


def get_sorted_candidates():
    StockMgr.skip = False
    records = Candidate.query.all()
    records = [CandidateUnit(rec) for rec in records]

    records = sorted(records)

    return records
