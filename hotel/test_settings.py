from .settings import *
# Exclusivamente para pruebas automáticas; la aplicación normal usa MySQL.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
