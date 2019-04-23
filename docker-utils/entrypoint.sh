#!/bin/bash

export SITE_DIR=${SITE_DIR:-"/site/"}
export PYTHONPATH="${SITE_DIR}proj/:${PYTHONPATH}"
export SITE_DIR=${SITE_DIR}

cd ${SITE_DIR}proj/

if [ "$1" == 'init' ]; then
    echo "Run Migrations"
    python ${SITE_DIR}proj/manage.py migrate
    python ${SITE_DIR}proj/manage.py collectstatic --noinput
elif [ "$1" == 'manage' ]; then
    shift
    echo "Manage.py $@"
    python ${SITE_DIR}proj/manage.py $@
elif [ "$1" == 'python' ]; then
    shift
    echo "Manage.py $@"
    python ${SITE_DIR}proj/manage.py shell_plus
elif [ "$1" == "lint" ]; then
    shift
    echo "Pylint"
    pylint ${SITE_DIR}proj/evesch/
else
    exec "$@"
fi

