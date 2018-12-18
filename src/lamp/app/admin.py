from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from lamp.app import app
from lamp.model.grid import Grid
from lamp.model.candidate import Candidate
from lamp.model import db


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='lamp', template_mode='bootstrap3')
admin.add_view(ModelView(Grid, db.session))
admin.add_view(ModelView(Candidate, db.session))
