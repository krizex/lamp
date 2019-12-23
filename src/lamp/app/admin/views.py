from lamp.app.admin import admin
from lamp.model import Candidate, Grid, Trend, Rebound
from lamp.model import db
from lamp.app.admin.modelview import AuthModelView, AuthModelViewSortCode

def init_views():
    admin.add_view(AuthModelView(Candidate, db.session))
    admin.add_view(AuthModelView(Grid, db.session))
    admin.add_view(AuthModelView(Trend, db.session))
    admin.add_view(AuthModelViewSortCode(Rebound, db.session))


