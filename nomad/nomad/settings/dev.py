from .base import *

#: Django secret key for sessions encryption.
SECRET_KEY = 'django-insecure-1ho2(*gqkz*f*6w6pwy2)6h*ts0vfwie__6ms12)vdi7wt7ko5'

#: Enable DEBUG on development, don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

BASE_URL="http://localhost:8000"

# Add CORS headers only for dev environment!
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# Permissive CORS policy in dev only !
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'nomad.sqlite3'),
    }
}


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nepasrepondre.djeghdir@gmail.com'
EMAIL_HOST_PASSWORD = 'ujthvzjvxzvzwrgu'
EMAIL_PORT = 587
