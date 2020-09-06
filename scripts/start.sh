#!/bin/bash

# until nc -z -v -w30 db 5432; do (err: nc not found)
#  echo 'Waiting for Postgres...'
#  sleep 1
# done

../sac_election.env
sleep 10; # get the above nc code to work
python3 manage.py migrate;
python3 manage.py runserver 0.0.0.0:8000;