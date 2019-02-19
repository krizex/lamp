# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from lamp.model import Candidate
from lamp.model import Grid
from lamp.model import db
from lamp.model import ALL_TABLES

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


def dump_data(cls):
    dmp = []
    recs = cls.query.all()
    for rec in recs:
        d = OrderedDict()
        for col in rec.__table__.columns:
            attr = col.key
            if attr.startswith('_') or attr == 'id':
                continue
            d[attr] = getattr(rec, attr)
        dmp.append(d)

    return dmp


def tbl_name2cls(name):
    if name in ALL_TABLES:
        return ALL_TABLES[name]

    raise RuntimeError('Unknow table %s' % name)


def dump_table(tblname):
    tbl_cls = tbl_name2cls(tblname)
    return dump_data(tbl_cls)
