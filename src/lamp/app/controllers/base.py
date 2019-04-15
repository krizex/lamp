from lamp.log import log
from lamp.stocks.stock import Stock


class ObjectBaseUnit(object):
    def __init__(self, code, name, own):
        self.code = code
        self.name = name
        self.own = own
        self.fill_info()

    def fill_info(self):
        log.debug('Fetching %s', self.code)
        self.stock = Stock(self.code)
        try:
            if not self.name:
                self.name = self.stock.name
            self.cur_price = self.stock.get_last_day_close()
            self.cur_p_change = self.stock.get_last_day_p_change()
            self.cur_price_ma40 = self.stock.get_last_day_ma40()
        except Exception as e:
            log.exception('Cannot get info for %s' % self.code)

    def trend_high_ndays(self, n):
        return self.stock.get_highest_in_n_days(n)

    def trend_low_ndays(self, n):
        return self.stock.get_lowest_in_n_days(n)

    def __eq__(self, other):
        return self.code == other.code and self.own == other.own

    def __lt__(self, other):
        if self.own < other.own:
            return True
        elif self.own > other.own:
            return False
        else:
            return self.code < other.code
