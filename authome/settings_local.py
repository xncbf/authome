from authome.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1tcc-!d(x+=nj9@60dzuqo7$$(4v632-p=m%6y1ee!o!9fiepx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR.child('db.sqlite3'),
#     }
# }

# STATIC_ROOT = BASE_DIR.child("static")

# MEDIA_ROOT = BASE_DIR.child('images')
