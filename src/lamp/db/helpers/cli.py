# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from lamp.model import Candidate
from lamp.model import Grid
from lamp.model import db

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

    print json.dumps(dmp, indent=4)


def tbl_name2cls(name):
    if name == 'grid':
        return Grid
    elif name == 'candidate':
        return Candidate

    raise RuntimeError('Unknow table %s' % name)


def dump_table(tblname):
    tbl_cls = tbl_name2cls(tblname)
    dump_data(tbl_cls)
