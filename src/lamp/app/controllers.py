#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lamp.model import Candidate, Grid
from lamp.stocks.stock import Stock, StockMgr
from lamp.log import log
from lamp.app.candidate import CandidateUnit, WaveUnit, TrendUnit
from lamp.app.grid import GridUnit


def unit_dispatcher(rec):
    if rec.own == 1:
        return WaveUnit(rec)
    elif rec.own == 2:
        return TrendUnit(rec)
    else:
        return CandidateUnit(rec)


def get_sorted_candidates():
    StockMgr.skip = False
    records = Candidate.query.all()
    records = [unit_dispatcher(rec) for rec in records]

    records = sorted(records)

    return records



def get_grids():
    StockMgr.skip = False
    records = Grid.query.all()
    records = [GridUnit(rec) for rec in records]


    return records
