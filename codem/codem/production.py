from codem.codem.settings import *
import os
import dj_database_url

# Access the environment variables using 'os.environ' in your Django settings.py
SECRET_KEY = os.environ.get('SECRET_KEY') # Django SECRET_KEY

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Debug Mode
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']


