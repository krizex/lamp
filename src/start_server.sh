#!/bin/bash

exec gunicorn -p app.pid -w 1 -b 0.0.0.0:8000 lamp.app.run:app &
