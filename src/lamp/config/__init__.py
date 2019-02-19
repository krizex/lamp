#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from . import db

data_node = '/persist'
basis_persistent_file = os.path.join(data_node, 'basis.json')


def debug_on():
    if 'FLASK_DEBUG' in os.environ:
        if os.environ['FLASK_DEBUG'] == '1':
            return True
        else:
            return False
    else:
        return True

logger = {
    'path': '/var/log',
    'file': 'lamp.log',
    'level': logging.DEBUG,
    'maxBytes': 1024 * 1024 * 20,
    'backupCount': 5,
    'term_logger': debug_on(),
}

