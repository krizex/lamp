#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lamp.datamanager.dataset import Candidate
from lamp.stocks.stock import Stock


class Unit(object):
    def __init__(self, rec):
        self.code = rec['code']
        self.start_pe = rec['start_pe']
        self.start_price = rec['start_price']
        self.stop_pe = rec['stop_pe']
        self.own = rec['own']
        self.note = rec['note']
        self.fill_info()

    def fill_info(self):
        # TODO: optimize
        self.name = 'UNKNOWN'
        self.cur_price = 0.1
        self.cur_date = 'UNKNOWN'
        try:
            stock = Stock(self.code)
            self.name = stock.name
            self.cur_price = stock.get_last_day_close()
            self.cur_date = stock.get_last_day_date()
        except:
            pass

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
    def volatility_range(self):
        return '+%.2f%% ~ -%.2f%%' % (self.volatility_up * 100, self.volatility_down * 100)

    @property
    def quite_distance(self):
        if self.cur_price >= self.start_price:
            return (self.stop_price - self.cur_price) / self.cur_price
        else:
            return -(self.cur_price - self.stop_loss_price) / self.cur_price

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
            return cmp(abs(self.quite_distance), abs(other.quite_distance))
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



def get_sorted_candidates():
    records = Candidate().get_all()
    records = [Unit(rec) for rec in records]
    def cmp(x, y):
        if x == y:
            return 0
        elif x < y:
            return -1
        else:
            return 1


    records = sorted(records, cmp=cmp)

    return records

