#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from jinja2 import StrictUndefined
from lamp import config
from lamp.log import log

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % config.database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
from lamp.model import db
db.init_app(app)

def _init_database():
    with app.app_context():
        # db.create_all()
        from lamp.db.helpers import cli
        cli.update_candidates_from_file('data.json')
        cli.update_grids_from_file('grid.json')
    log.info('DB initialized.')


_init_database()

from lamp.app import routers



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000, passthrough_errors=True)
