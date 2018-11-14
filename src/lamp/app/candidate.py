from lamp.stocks.stock import Stock
from lamp.log import log
from abc import ABCMeta, abstractproperty, abstractmethod
import traceback

class AbstractCandidate(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def own_type(self):
        pass


class CandidateUnit(AbstractCandidate):
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
    def start_pe_str(self):
        return '%.2f' % self.start_pe

    @property
    def stop_pe_str(self):
        return '%.2f' % self.stop_pe

    @property
    def stop_price(self):
        return self.start_price * (1 + self.volatility_up)

    @property
    def stop_price_str(self):
        return '%.2f' % self.stop_price

    @property
    def stop_loss_price(self):
        return self.start_price / (1 + self.volatility_up)

    @property
    def stop_loss_price_str(self):
        return '%.2f' % self.stop_loss_price

    @property
    def volatility_up(self):
        return self.stop_pe / self.start_pe - 1

    @property
    def volatility_down(self):
        return (self.start_price - self.stop_loss_price) / self.start_price

    @property
    def volatility_range(self):
        return '+%.2f%%' % (self.volatility_up * 100), '-%.2f%%' % (self.volatility_down * 100)

    @property
    def progress(self):
        if self.cur_price >= self.start_price:
            hover = self.stop_price
        else:
            hover = self.stop_loss_price

        return (self.cur_price - self.start_price) / (hover - self.start_price)

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

    def _calc_color(self):
        if self.own:
            if self.cur_price >= self.start_price:
                inc = (self.cur_price - self.start_price) / self.start_price
                if inc < self.volatility_up / 2:
                    return 'info'
                else:
                    return 'success'
            else:
                decr = (self.start_price - self.cur_price) / self.start_price
                if decr < self.volatility_down / 2:
                    return 'warning'
                else:
                    return 'danger'
        else:
            if abs(self.enter_distance) <= 0.05:
                return 'active'
            else:
                return 'light'

    @property
    def color_class(self):
        color = self._calc_color()
        return 'class=table-%s' % color

    @property
    def trend_info(self):
        low = self.trend_stop
        high = self.trend_start
        l = (high - low) / 2.0
        cur = self.cur_price - low
        if cur >= l:
            color = 'bg-success'
            pos = (cur - l) / l
        else:
            color = 'bg-danger'
            pos = (l - cur) / l

        return color, pos

    @property
    def trend_start(self):
        return self.stock.get_highest_in_n_days(22)

    @property
    def trend_stop(self):
        return self.stock.get_lowest_in_n_days(11)

    @property
    def own_type(self):
        return ''

    @property
    def start_after(self):
        return '%+.2f%%' % (self.enter_distance * 100)



class WaveUnit(CandidateUnit):
    @property
    def own_type(self):
        return 'wave'

    @property
    def start_after(self):
        return '-'


class TrendUnit(CandidateUnit):
    @property
    def own_type(self):
        return 'trend'

    @property
    def start_after(self):
        return '-'

    @property
    def start_pe_str(self):
        return '-'

    @property
    def stop_pe_str(self):
        return '-'

    @property
    def volatility_range(self):
        return ('-', '-')

    @property
    def stop_price_str(self):
        return '-'

    @property
    def stop_loss_price_str(self):
        return '%.2f' % self.trend_stop
