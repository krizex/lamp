#!/bin/bash
export PYTHONPATH=`pwd`
export FLASK_APP=lamp.app
export FLASK_DEBUG=1
flask run -h 0.0.0.0 -p 8000
