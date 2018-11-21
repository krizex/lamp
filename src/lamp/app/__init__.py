#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from lamp import config

app = Flask(__name__)

from lamp.app.views import display_candidates_data
from lamp.app.views import display_grids_data


@app.route('/')
@app.route('/wave/')
def index():
    return display_candidates_data()


@app.route('/grid/')
def grid():
    return display_grids_data()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000, passthrough_errors=True)
