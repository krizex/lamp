from lamp.app import app
from lamp import config
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % config.database
db = SQLAlchemy(app)

# Import models here
from lamp.model.candidate import Candidate
