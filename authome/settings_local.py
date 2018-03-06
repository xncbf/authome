from dotenv import load_dotenv
from unipath import Path
load_dotenv()

load_dotenv(verbose=True)

BASE_DIR = Path(__file__).ancestor(2)
env_path = BASE_DIR.child('.env')
load_dotenv(dotenv_path=env_path)

from authome.settings import *
print('LOCAL!!!!')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1tcc-!d(x+=nj9@60dzuqo7$$(4v632-p=m%6y1ee!o!9fiepx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SITE_ID = 3
ALLOWED_HOSTS = ['*']
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_DOMAIN = '.example.com'
INTERNAL_IPS = ['127.0.0.1']
BROKER_URL = 'django://'
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR.child('db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ['AUTHOME_DATABASE_NAME'],
#         'USER': os.environ['AUTHOME_DATABASE_USER'],
#         'PASSWORD': os.environ['AUTHOME_DATABASE_PASSWORD'],
#         'HOST': 'fortest.cqzciqkjmzjq.ap-northeast-2.rds.amazonaws.com',
#         'PORT': os.environ['AUTHOME_DATABASE_PORT'],
#     }
# }

# STATIC_ROOT = BASE_DIR.child("static")

# MEDIA_ROOT = BASE_DIR.child('images')

XRAY_RECORDER = {
    'AWS_XRAY_DAEMON_ADDRESS': '127.0.0.1:3000',
    'AUTO_INSTRUMENT': False,
    'AWS_XRAY_CONTEXT_MISSING': 'RUNTIME_ERROR',
    'PLUGINS': (),
    'SAMPLING': True,
    'SAMPLING_RULES': None,
    'AWS_XRAY_TRACING_NAME': 'authome',
    'DYNAMIC_NAMING': '*.autho.me',
}
