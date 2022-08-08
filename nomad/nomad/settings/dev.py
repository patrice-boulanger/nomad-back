from .base import *

#: Django secret key for sessions encryption.
SECRET_KEY = 'django-insecure-1ho2(*gqkz*f*6w6pwy2)6h*ts0vfwie__6ms12)vdi7wt7ko5'

#: Enable DEBUG on development, don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'nomad.sqlite3'),
    }
}

