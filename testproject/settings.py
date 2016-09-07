import pkg_resources

SECRET_KEY = 'x'
USE_I18N = True
ROOT_URLCONF = 'testproject.urls'
INSTALLED_APPS = [
    'django_babel',
    'testproject',
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
    pkg_resources.resource_filename(__name__, 'locale'),
]
