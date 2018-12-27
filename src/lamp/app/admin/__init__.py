from flask_admin import Admin
from lamp.app import app
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='lamp', template_mode='bootstrap3')

from lamp.app.admin.views import init_views

init_views()
