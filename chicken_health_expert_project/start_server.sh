#!/bin/bash

# clear session files
rm -rf /tmp/django-sessions/*

# start the django server
python3 manage.py runserver