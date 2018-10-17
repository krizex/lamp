#!/bin/bash

PROG_NAME=$0

print_help ()
{
    echo "Usage : $PROG_NAME <start|stop|debug>"
    exit 1
}

if [ $# -ne 1 ]
then
    print_help
fi


case "$1" in
    start)
        echo "starting server"
        exec gunicorn -p app.pid -w 1 -b 0.0.0.0:8000 lamp.app.run:app &
        ;;
    stop)
        echo "killing server"
        kill `cat app.pid`
        ;;
    debug)
        echo "starting debug"
        export PYTHONPATH=`pwd`
        export FLASK_APP=lamp.app
        export FLASK_DEBUG=1
        flask run -h 0.0.0.0 -p 8000
        ;;
    *)
        print_help
       ;;
esac