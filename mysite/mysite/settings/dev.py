from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-r_i)ru(tncrh9xn@92r1*m=e_e-efo&e2#!%ghdv+jo3fx^fin"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["upinterior.com.vn","upinterior.vn"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
