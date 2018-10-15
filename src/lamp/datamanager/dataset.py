#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

from lamp.db.db import DBManager


class Candidate(object):
    def __init__(self):
        self.records = self._get_all()

    def _get_all(self):
        return DBManager.query_db('select * from candidates')

    def get_all(self):
        return self.records
