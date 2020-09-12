#!/bin/bash

# until nc -z -v -w30 db 5432; do (err: nc not found)
#  echo 'Waiting for Postgres...'
#  sleep 1
# done

../sac_election.env
sleep 10; # get the above nc code to work
python3 manage.py migrate;

# development
#python3 manage.py runserver 0.0.0.0:8000;

# production 4 workers
gunicorn -w 4 sac_elections.wsgi -b 0.0.0.0:8000