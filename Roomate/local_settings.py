import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'roomate',
        'USER': 'postgremanager',
        'PASSWORD': 'A71jpC1k',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEBUG = True