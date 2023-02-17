#!/bin/sh

# Make .mo files for translations
python3 manage.py compilemessages


# Make migrations
python3 manage.py migrate

# Start server with debug mode
python3 manage.py runserver 0.0.0.0:8000
# Start server with production mode
#daphne -b 0.0.0.0 -p 8000 core.asgi:application
