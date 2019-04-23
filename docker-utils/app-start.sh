#!/bin/bash

echo "Starting uWSGI"
PROJECT_NAME="evesch"

python ${SITE_DIR}proj/manage.py collectstatic --noinput

uwsgi --chdir ${SITE_DIR}proj/ \
    --module=${PROJECT_NAME}.wsgi:application \
    --master \
    --env DJANGO_SETTINGS_MODULE=${PROJECT_NAME}.settings \
    --vacuum \
    --max-requests=5000 \
    --${CONNECT_METHOD:=socket} 0.0.0.0:8000 \
    --processes ${NUM_PROCS} \
    --threads ${NUM_THREADS} \
    --python-autoreload=1 \
    --honour-stdin

#    --static-map /static=${SITE_DIR}htdocs/static/ \
#    --static-map /media=${SITE_DIR}htdocs/media/ \

