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
            if val >= 4.0:
                return '%.2f' % val
            else:
                return '%.3f' % val

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
    def trend_start(self):
        return self.grid.trend_start_ndays(22)

    @property
    def trend_stop(self):
        return self.grid.trend_stop_ndays(11)

    @property
    def trend_info(self):
        low = self.trend_stop
        high = self.trend_start
        l = (high - low) / 2.0
        cur = self.grid.cur_price - low
        if cur >= l:
            color = 'bg-success'
            pos = (cur - l) / l
        else:
            color = 'bg-danger'
            pos = (l - cur) / l

        return color, pos


def display_grids_data():
    recs = get_grids()
    recs = [GridView(r) for r in recs]
    return render_template('grids_data.html', recs=recs)
