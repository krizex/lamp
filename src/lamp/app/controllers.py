#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lamp.datamanager.dataset import Candidate


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
        # TODO: fetch the info
        self.name = 'NAME'
        self.cur_price = 1.0

    @property
    def stop_price(self):
        return self.start_price * (1 + self.volatility)

    @property
    def stop_loss_price(self):
        return self.start_price / (1 + self.volatility)

    @property
    def volatility(self):
        return self.stop_pe / self.start_pe - 1

    @property
    def quite_distance(self):
        if self.cur_price >= self.start_price:
            return self.stop_price / self.cur_price - 1
        else:
            return self.cur_price / self.stop_loss_price - 1

    @property
    def enter_distance(self):
        if self.cur_price >= self.start_price:
            return self.cur_price / self.start_price - 1
        else:
            return self.start_price / self.cur_price - 1

    def __cmp__(self, other):
        if self.own > other.own:
            return -1
        elif self.own < other.own:
            return 1
        # now self and other .own equals
        elif self.own == 1:
            return self.quite_distance - other.quite_distance
        elif self.own == 0:
            return self.enter_distance - other.enter_distance


def get_sorted_candidates():
    records = Candidate().get_all()
    records = [Unit(rec) for rec in records]
    records = sorted(records)

    return records

