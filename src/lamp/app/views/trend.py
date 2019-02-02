#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from lamp.app.controllers.trend import get_trends
from lamp.utils.absattr import AbsAttrPassThrough


class TrendView(AbsAttrPassThrough):
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
    def next_buy(self):
        return '%.2f' % self.trend.next_buy()

    @property
    def flush_price(self):
        return '%.2f' % self.trend.flush_price()

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
        return self.trend.cur_hold * self.unit

    @property
    def trend_position_of_cur_price(self):
        return self.trend.calc_trend_position_of_cur_price()


def get_trends_data():
    recs = get_trends()
    recs = [TrendView(r) for r in recs]
    return recs
