#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from lamp import config


def __init_config_dir():
    for d in (config.data_node,):
        if not os.path.exists(d):
            os.mkdir(d)

__init_config_dir()
