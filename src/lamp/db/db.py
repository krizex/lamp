#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sqlite3
from contextlib import closing
from lamp.config import database


class _DBManager(object):
    def __init__(self):
        self.db = sqlite3.connect(database)

    def query_db(self, query, args=(), one=False):
        cur = self.db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv


DBManager = _DBManager()

def init_db():
    from lamp.app import app
    with closing(DBManager.db) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        init_db()
    else:
        print "What's your plan?"

    exit(0)
