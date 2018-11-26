#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from jinja2 import StrictUndefined
from lamp import config

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % config.database
from lamp.model import db
db.init_app(app)


from lamp.app import routers



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000, passthrough_errors=True)
