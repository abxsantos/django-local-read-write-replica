import os
from pathlib import Path

from pythonjsonlogger.jsonlogger import JsonFormatter

from django_local_read_write_replica.apps.my_app.apps import MyAppConfig
from django_local_read_write_replica.support.utils import eval_env_as_bool

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "4z57zflmt-w81=r27)090wmve@js1af^%sktovelm46p7i^nw%"
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    MyAppConfig.name,
    'django_q',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_local_read_write_replica.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_local_read_write_replica.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}
if eval_env_as_bool(os.getenv("DB_USE_REPLICA")):
    DATABASES["replica"] = {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME_REPLICA"),
        "USER": os.getenv("DB_USER_REPLICA"),
        "HOST": os.getenv("DB_HOST_REPLICA"),
        "PORT": os.getenv("DB_PORT_REPLICA"),
        "PASSWORD": os.getenv("DB_PASSWORD_REPLICA"),
        "TEST": {"MIRROR": "default"},
    }
    DATABASE_ROUTERS = ["django_local_read_write_replica.support.db_router.DatabaseRouter"]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] %(name)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["console"]},
        "app": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django": {"level": "INFO", "propagate": False, "handlers": ["console"]},
        "django.request": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.db.backends": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["console"],
        },
    },
}

Q_CLUSTER = {
    "name": "myscheduler",
    "orm": "replica",  # Use Django's ORM + database for broker
    "save_limit": int(os.getenv("Q_CLUSTER_SAVE_LIMIT", 0)),  # -1 to not save success tasks
    "max_attempts": int(os.getenv("Q_CLUSTER_MAX_ATTEMPTS", 5)),  # Attempts before failing
    "retry": int(os.getenv("Q_CLUSTER_RETRY", 15)),  # Seconds a broker will wait for a cluster to finish a task
    "timeout": int(os.getenv("Q_CLUSTER_TIMEOUT", 10)),  # Seconds a worker spend on a task before it’s terminated
    "poll": int(os.getenv("Q_CLUSTER_POOL", 0.2)),  # Seconds which django Q will make a query to verify the time
}
