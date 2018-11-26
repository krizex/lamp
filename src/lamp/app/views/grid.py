#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from lamp.app.controllers.grid import get_grids


class GridView(object):
    def __init__(self, grid):
        self.grid = grid
        self.code = grid.code
        self.name = grid.name
        self.size = grid.size
        self.unit = grid.unit
        self.note = grid.note
        self.cur_price = grid.cur_price
        self.cur_p_change = grid.cur_p_change
        self.width = grid.width

    @property
    def hold_count(self):
        holds = self.grid.calc_hold_cnt()
        return ['%d' % (hold * self.grid.unit) for hold in holds]

    def get_ruler_scale(self, pos):
        if pos < 0 or pos >= len(self.grid.ruler):
            return 'NA'
        else:
            return '%.3f' % self.grid.ruler[pos]

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
