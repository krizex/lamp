# -*- coding: utf-8 -*-

from lamp import app
from lamp.model import Candidate
from lamp.model import Grid
from lamp.model import db
import json

def list_candidates():
    recs = Candidate.query.all()
    for r in recs:
        print r


def get_values(d, *keys):
    return [d[k] for k in keys]


def update_candidates_from_file(f):
    d = {}
    with open(f) as f:
        recs = json.load(f)
        for r in recs:
            d[r['code']] = r

    candidates = Candidate.query.all()

    def find_candidate(code):
        for c in candidates:
            if code == c.code:
                return c

        return None

    # delete
    for candidate in candidates:
        if candidate.code not in d:
            db.session.delete(candidate)

    # add & update
    for code, r in d.iteritems():
        c = find_candidate(code)
        if 'name' not in r:
            r['name'] = ''

        if c is None:
            # add
            c = Candidate(*get_values(r, 'code', 'name', 'start_pe', 'stop_pe', 'start_price', 'own', 'note'))
            db.session.add(c)
        else:
            # update
            c.update(r)

    db.session.commit()


def update_grids_from_file(f):
    d = {}
    with open(f) as f:
        recs = json.load(f)
        for r in recs:
            d[r['code']] = r

    grids = Grid.query.all()

    def find_grid(code):
        for c in grids:
            if code == c.code:
                return c

        return None

    # delete
    for grid in grids:
        if grid.code not in d:
            db.session.delete(grid)

    # add & update
    for code, r in d.iteritems():
        c = find_grid(code)
        if 'name' not in r:
            r['name'] = ''

        if c is None:
            # add
            c = Grid(*get_values(r, 'code', 'name', 'high', 'low', 'size', 'unit', 'own', 'note'))
            db.session.add(c)
        else:
            # update
            c.update(r)

    db.session.commit()

