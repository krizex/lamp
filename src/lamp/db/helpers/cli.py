# -*- coding: utf-8 -*-

from lamp import app
from lamp.model import Candidate
from lamp.model import db
import json

def list_candidates():
    recs = Candidate.query.all()
    for r in recs:
        print r


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
        if c is None:
            # add
            c = Candidate(r['code'], r['start_pe'], r['stop_pe'], r['start_price'], r['own'], r['note'])
            db.session.add(c)
        else:
            # update
            c.update(r)

    db.session.commit()


