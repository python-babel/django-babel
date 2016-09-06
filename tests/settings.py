import os

SECRET_KEY = 'x'
USE_I18N = True
ROOT_URLCONF = 'tests.urls'
INSTALLED_APPS = [
    'django_babel',
    'tests',
]
MIDDLEWARE_CLASSES = [
    'django.middleware.locale.LocaleMiddleware',
    'django_babel.middleware.LocaleMiddleware',
]
TEMPLATES = [
    {
        'NAME': 'default',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
            ],
        },
    },
]
LOCALE_PATHS = [
    os.path.join(os.path.dirname(__file__), 'locale'),
]
