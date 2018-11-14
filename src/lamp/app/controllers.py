#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lamp.model import Candidate
from lamp.stocks.stock import Stock, StockMgr
from lamp.log import log
from lamp.app.candidate import CandidateUnit, WaveUnit, TrendUnit


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

