import dj_database_url
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q*4)i8c!o%-pzz-#yy2g#@hi@&txxxzhzn=p0@d$)cw%k8+h5q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']

# dj-database-url configuration
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
