
from flask import Flask
from jinja2 import StrictUndefined
from lamp import config
from lamp.log import log

app = Flask(__name__)
# app.jinja_env.undefined = StrictUndefined


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % config.database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

