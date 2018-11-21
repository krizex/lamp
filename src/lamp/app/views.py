#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from lamp.app.controllers import get_sorted_candidates
from lamp.app.controllers import get_grids


def display_candidates_data():
    recs = get_sorted_candidates()
    return render_template('candidates_data.html', recs=recs)


def display_grids_data():
    recs = get_grids()
    return render_template('grids_data.html', recs=recs)
