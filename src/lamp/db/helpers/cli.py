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


def update_from_file(f, cls):
    with open(f) as f:
        recs = json.load(f)

    cls.query.delete()
    for rec in recs:
        if 'name' not in rec:
            rec['name'] = ''

        c = cls(**rec)
        db.session.add(c)

    db.session.commit()


def update_candidates_from_file(f):
    update_from_file(f, Candidate)


def update_grids_from_file(f):
    update_from_file(f, Grid)

