#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lamp.app import app

__author__ = 'David Qian'

"""
Created on 12/20/2016
@author: David Qian

"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, passthrough_errors=True)
