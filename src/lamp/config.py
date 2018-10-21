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

logger = {
    'path': os.path.join(root_node['path'], 'logs'),
    'file': 'lamp.log',
    'level': logging.DEBUG,
    'maxBytes': 1024 * 1024 * 20,
    'backupCount': 5,
}

database = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'database.db')
