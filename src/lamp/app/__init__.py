#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .run import create_app
app = create_app()

from lamp.model import db

db.init_app(app)

from . import admin

from . import routers


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000, passthrough_errors=True)
