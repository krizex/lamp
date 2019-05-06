#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from lamp.app.controllers.trend import get_trends
from .base import BaseView


class TrendView(BaseView):
    _PASS_THROUGH_ATTRS = [
        'code',
        'name',
        'start_price',
        'unit',
        'note',
        'cur_price',
        'cur_p_change',
        'ratio',
        'own',
    ]

    def __init__(self, trend):
        self.trend = trend

    @property
    def _datasource(self):
        return self.trend

    @property
    def prec(self):
        if 'ETF' in self.name:
            return 3
        else:
            return 2

    @property
    def next_buy_price(self):
        return '%.*f' % (self.prec, self.trend.next_buy_price())

    @property
    def next_buy_cnt(self):
        return self.trend.next_buy_cnt()

    @property
    def cur_flush_price(self):
        return '%.*f' % (self.prec, self.trend.cur_flush_price())

    @property
    def cur_flush_cnt(self):
        return self.trend.cur_flush_cnt()

    @property
    def trend_high(self):
        return self.trend.trend_high_ndays(self.trend.trend_up_days_cnt)

    @property
    def trend_low(self):
        return self.trend.trend_low_ndays(self.trend.trend_down_days_cnt)

    @property
    def trend_info(self):
        low = self.trend_low
        high = self.trend_high
        l = (high - low) / 2.0
        cur = self.trend.cur_price - low
        if cur >= l:
            color = 'bg-success'
            pos = (cur - l) / l
        else:
            color = 'bg-danger'
            pos = (l - cur) / l

        return color, pos

    @property
    def cur_hold(self):
        hold_rate, hold_cnt = self.trend.calc_cur_hold()
        return '%d%%' % (int(hold_rate * 100)), hold_cnt

    @property
    def op_position_of_cur_price(self):
        return self.trend. calc_op_position_of_cur_price()

    @property
    def stop_benefit_price(self):
        return self.trend.stop_benefit_price()

    def break_highest(self):
        return self.trend.break_highest()

    @property
    def approx_benefit_rate(self):
        return self.trend.calc_approx_benefit_rate()

    @property
    def cur_invest(self):
        return int(self.trend.calc_cur_investment())

def get_trends_data():
    recs = get_trends()
    recs = [TrendView(r) for r in recs]
    return recs
