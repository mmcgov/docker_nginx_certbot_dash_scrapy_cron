#!/bin/bash

bash ./wait_on_scraper.sh
gunicorn --workers 3 -b 0.0.0.0:8000 wsgi:app

exec $@
