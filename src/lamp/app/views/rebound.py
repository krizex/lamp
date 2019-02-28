#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from lamp.app.controllers.rebound import get_rebounds
from .base import BaseView


class ReboundView(BaseView):
    _PASS_THROUGH_ATTRS = [
        'code',
        'name',
        'days',
        'ratio',
        'note',
        'cur_price',
        'cur_p_change',
    ]

    def __init__(self, rebound):
        self.rebound = rebound

    # @property
    # def last_n_days_date(self):
    #     return [1]
    #     ret = self.get_last_n_days_date(11)
    #     log.debug('last_n_days_date')
    #     log.debug(ret)
    #     return ret

    @property
    def _datasource(self):
        return self.rebound

    @property
    def prec(self):
        if 'ETF' in self.name:
            return 3
        else:
            return 2

    @property
    def lowest_price(self):
        return self.rebound.lowest_price()

    @property
    def rebound_price(self):
        rebound = self.rebound.rebound_price()
        return '%.*f' % (self.prec, rebound)

    @property
    def trend_position_of_cur_price(self):
        return self.rebound.calc_trend_position_of_cur_price()


def get_rebounds_data():
    recs = get_rebounds()
    recs = [ReboundView(r) for r in recs]
    return recs
