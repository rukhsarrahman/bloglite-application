import os
from datetime import timedelta
from celery.schedules import crontab
current_dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERY_TIMEZONE = 'UTC'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 1000
    CACHE_KEY_PREFIX = 'bloglite_api_'
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "email@bloglite.com"
    SENDER_PASSWORD = ""

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(current_dir,"../database_directory")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR,'database.sqlite3')
    DEBUG = True
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    SECRET_KEY = "ur8390ru93fj0"
    CELERY_TIMEZONE = 'UTC'
    CELERYBEAT_SCHEDULE = {
        'making daily emails': {
            'task': 'application.tasks.dailyEmail',
            'schedule': crontab(hour = 6, minute = 8),
        },
        'making monthly reports': {
            'task': 'application.tasks.generate_report_data',
            'schedule': crontab(hour = 6, minute = 9),
        }
    }