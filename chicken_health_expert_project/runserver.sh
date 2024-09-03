#!/bin/bash

# create temporary session directory
mkdir -p /tmp/django_sessions

# run django development server
python3 manage.py runserver