from .base import *

SECRET_KEY = 'z%bh1e#iq^en$yc40e6+yui&pje=^d29o)0o@vmxx(_(7y)ybp'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
