from flask_admin.contrib.sqla import ModelView
from lamp.app.admin.basicauth import basic_auth
from lamp.exceptions.auth import AuthException
from flask import redirect


class AuthModelView(ModelView):
    # can_delete = False
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())
