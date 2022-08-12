# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

import os
from django.utils.translation import gettext_lazy as _

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

#: Default language.
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#: Paths to search for the translation files.
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locales'),
)

#: Languages supported by the application.
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

