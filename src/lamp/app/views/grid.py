#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from lamp.app.controllers.grid import get_grids
from lamp.utils.absattr import AbsAttrPassThrough


class GridView(AbsAttrPassThrough):
    _PASS_THROUGH_ATTRS = [
        'code',
        'name',
        'size',
        'unit',
        'note',
        'cur_price',
        'cur_p_change',
        'width',
        'is_fund',
        'own',
    ]

    def __init__(self, grid):
        self.grid = grid

    @property
    def _datasource(self):
        return self.grid

    @property
    def hold_count(self):
        holds = self.grid.calc_hold_cnt()
        return ['%d' % (hold * self.grid.unit) for hold in holds]

    def get_ruler_scale(self, pos):
        if pos < 0 or pos >= len(self.grid.ruler):
            return 'NA'
        else:
            val = self.grid.ruler[pos]
            if 'ETF' in self.name:
                return '%.3f' % val
            else:
                return '%.2f' % val

    @property
    def next_sell(self):
        rets = []
        for pos in self.grid.calc_hold_cnt():
            rets.append(self.get_ruler_scale(pos - 1))

        return rets

    @property
    def next_buy(self):
        rets = []
        for pos in self.grid.calc_hold_cnt():
            rets.append(self.get_ruler_scale(pos + 1))

        return rets

    @property
    def next_op_distance(self):
        return self.grid.calc_next_op_distance()

    @property
    def trend_high(self):
        return self.grid.trend_high_ndays(self.grid.trend_up_days_cnt)

    @property
    def trend_low(self):
        return self.grid.trend_low_ndays(self.grid.trend_down_days_cnt)

    @property
    def trend_info(self):
        low = self.trend_low
        high = self.trend_high
        l = (high - low) / 2.0
        cur = self.grid.cur_price - low
        if cur >= l:
            color = 'bg-success'
            pos = (cur - l) / l
        else:
            color = 'bg-danger'
            pos = (l - cur) / l

        return color, pos

    @property
    def ass_date(self):
        # omit the year field
        return self.grid.fund.ass_val_date[5:]

    @property
    def premium(self):
        premium = self.grid.calc_premium()
        return premium
        # return '%+.2f%%' % (premium * 100,)


def get_grids_data():
    recs = get_grids()
    recs = [GridView(r) for r in recs]
    return recs

