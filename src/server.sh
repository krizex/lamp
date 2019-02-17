#!/bin/bash
HOST=0.0.0.0
PORT=8001

PROG_NAME=$0

print_help ()
{
    echo "Usage : $PROG_NAME <start|stop|debug>"
    exit 1
}

start ()
{
    export FLASK_DEBUG=0
    echo "starting server"
    exec gunicorn -p app.pid -w 2 -b $HOST:$PORT --timeout 60 lamp.app.run:app
}

stop ()
{
    echo "killing server"
    kill `cat app.pid`
}

start_debug_server ()
{
    echo "starting debug"
    export PYTHONPATH=`pwd`
    export FLASK_APP=lamp.app
    export FLASK_DEBUG=1
    flask run -h $HOST -p $PORT
}

if [ $# -ne 1 ]
then
    print_help
fi


case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    debug)
        start_debug_server
        ;;
    restart)
        stop
        start
        ;;
    *)
        print_help
       ;;
esac
