from flask_basicauth import BasicAuth
from lamp.app import app

app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'else'

basic_auth = BasicAuth(app)
