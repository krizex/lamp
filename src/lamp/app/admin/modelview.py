from flask_admin.contrib.sqla import ModelView
from lamp.app.admin.basicauth import basic_auth
from lamp.exceptions.auth import AuthException
from flask import redirect
from lamp.stocks.stock import StockMgr

def get_name(view, context, model, name):
    if model.name:
        return model.name
    else:
        try:
            return StockMgr.get_stock_name(model.code)
        except:
            return 'UNKNOWN'


class AuthModelView(ModelView):
    # can_delete = False
    column_default_sort = ('own', True)

    form_widget_args = {
        'note' : {
          'rows': 10
          }
        }

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

    column_formatters = {
        'name': get_name
    }


class AuthModelViewSortCode(AuthModelView):
    column_default_sort = 'code'
