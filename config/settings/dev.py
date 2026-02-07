from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


DB_SSLMODE = ""  

DATABASES["default"]["OPTIONS"] = {}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework.permissions.AllowAny",
]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}