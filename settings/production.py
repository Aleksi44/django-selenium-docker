from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_db',
        'USER': 'app_user',
        'PASSWORD': 'changeme',
        'HOST': "app_db",
        'PORT': '5432',
    }
}

APP_BROKER_URL = 'pyamqp://app_user:changeme@app_rabbitmq:5672'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://:changeme@app_redis:6379"],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}
