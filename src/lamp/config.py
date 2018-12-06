#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os


root_node = {
    'path': os.path.join(os.path.dirname(__file__), 'running')
}

data_node = {
    'path': os.path.join(root_node['path'], 'data')
}

file_store = {
    'path': os.path.join(data_node['path'], 'images')
}

scanner = {
    'interval': 24 * 3600
}

basis_persistent_file = os.path.join(os.path.dirname(__file__), 'data', 'basis.json')

def debug_on():
    if 'FLASK_DEBUG' in os.environ:
        if os.environ['FLASK_DEBUG'] == '1':
            return True
        else:
            return False
    else:
        return True

logger = {
    'path': os.path.join(root_node['path'], 'logs'),
    'file': 'lamp.log',
    'level': logging.DEBUG,
    'maxBytes': 1024 * 1024 * 20,
    'backupCount': 5,
    'term_logger': debug_on(),
}


database = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'database.db')
