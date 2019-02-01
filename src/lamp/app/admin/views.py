from lamp.app.admin import admin
from lamp.model.grid import Grid
from lamp.model.trend import Trend
from lamp.model.candidate import Candidate
from lamp.model import db
from lamp.app.admin.modelview import AuthModelView

def init_views():
    admin.add_view(AuthModelView(Grid, db.session))
    admin.add_view(AuthModelView(Trend, db.session))
    admin.add_view(AuthModelView(Candidate, db.session))


