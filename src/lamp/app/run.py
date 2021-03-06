import os
from flask import Flask
from jinja2 import StrictUndefined
from lamp import config
from lamp.log import log

def create_app():
    app = Flask(__name__)
    # app.jinja_env.undefined = StrictUndefined

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % config.database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SECRET_KEY'] = os.urandom(24)

    return app

