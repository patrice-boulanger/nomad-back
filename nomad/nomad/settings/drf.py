#: Django REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

#: Swagger settings, only used for online documentation. Only token authentication is supported.
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
       'Basic': {
           'type': 'basic'
       },
   }
}