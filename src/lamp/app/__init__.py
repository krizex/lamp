#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template

from lamp.app.views import display_candidates_data


app = Flask(__name__)


@app.route('/')
@app.route('/candidates')
def index():
    return display_candidates_data()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000, passthrough_errors=True)
