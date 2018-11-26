#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from abc import ABCMeta, abstractproperty, abstractmethod

from lamp.app.controllers.candidate import get_sorted_candidates


class AbstractCandidateView(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def own_type(self):
        pass


class CandidateView(AbstractCandidateView):
    def __init__(self, candidate):
        self.c = candidate

    @property
    def code(self):
        return self.c.code

    @property
    def name(self):
        return self.c.name

    @property
    def own(self):
        return self.c.own

    @property
    def note(self):
        return self.c.note

    @property
    def start_price(self):
        return self.c.start_price

    @property
    def cur_price(self):
        return self.c.cur_price

    @property
    def cur_benefit(self):
        return self.c.cur_benefit

    @property
    def cur_p_change(self):
        return self.c.cur_p_change

    @property
    def start_pe(self):
        return '%.2f' % self.c.start_pe

    @property
    def stop_pe(self):
        return '%.2f' % self.c.stop_pe

    @property
    def stop_price(self):
        return '%.2f' % self.c.stop_price

    @property
    def stop_loss_price(self):
        return '%.2f' % self.c.stop_loss_price

    @property
    def volatility_range(self):
        return '+%.2f%%' % (self.c.volatility_up * 100), '-%.2f%%' % (self.c.volatility_down * 100)

    @property
    def progress(self):
        c = self.c
        if c.cur_price >= c.start_price:
            hover = c.stop_price
        else:
            hover = c.stop_loss_price

        return (c.cur_price - c.start_price) / (hover - c.start_price)

    def _calc_color(self):
        c = self.c
        if c.own:
            if c.cur_price >= c.start_price:
                inc = (c.cur_price - c.start_price) / c.start_price
                if inc < c.volatility_up / 2:
                    return 'info'
                else:
                    return 'success'
            else:
                decr = (c.start_price - c.cur_price) / c.start_price
                if decr < c.volatility_down / 2:
                    return 'warning'
                else:
                    return 'danger'
        else:
            if abs(c.enter_distance) <= 0.05:
                return 'active'
            else:
                return 'light'

    @property
    def color_class(self):
        color = self._calc_color()
        return 'class=table-%s' % color

    @property
    def trend_info(self):
        low = self.c.trend_stop
        high = self.c.trend_start
        l = (high - low) / 2.0
        cur = self.c.cur_price - low
        if cur >= l:
            color = 'bg-success'
            pos = (cur - l) / l
        else:
            color = 'bg-danger'
            pos = (l - cur) / l

        return color, pos

    @property
    def own_type(self):
        return ''

    @property
    def start_after(self):
        return '%+.2f%%' % (self.c.enter_distance * 100)

    @property
    def trend_start(self):
        return self.c.trend_start

    @property
    def trend_stop(self):
        return self.c.trend_stop


class WaveView(CandidateView):
    @property
    def own_type(self):
        return 'wave'

    @property
    def start_after(self):
        return '-'


class TrendView(CandidateView):
    @property
    def own_type(self):
        return 'trend'

    @property
    def start_after(self):
        return '-'

    @property
    def start_pe(self):
        return '-'

    @property
    def stop_pe(self):
        return '-'

    @property
    def volatility_range(self):
        return ('-', '-')

    @property
    def stop_price(self):
        return '-'

    @property
    def stop_loss_price(self):
        return '%.2f' % self.c.trend_stop



def build_render(candidate):
    if candidate.own == 1:
        return WaveView(candidate)
    elif candidate.own == 2:
        return TrendView(candidate)
    else:
        return CandidateView(candidate)


def display_candidates_data():
    candidates = get_sorted_candidates()
    candidates = [build_render(c) for c in candidates]
    return render_template('candidates_data.html', recs=candidates)
