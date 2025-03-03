#!/bin/bash

# install requirements
pip install -r requirements.txt

# create tables
python3 manage.py makemigrations app
python3 manage.py migrate app

# load data
python3 manage.py loaddata user_data.json
python3 manage.py migrate

python3 manage.py loaddata review_data.json
python3 manage.py migrate

python3 manage.py loaddata room_data.json
python3 manage.py migrate

python3 manage.py loaddata booking_data.json
python3 manage.py migrate

# start server
python3 manage.py runserver
