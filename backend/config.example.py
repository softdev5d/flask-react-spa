import os
from datetime import timedelta

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'frontend')
STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL_PATH = '/static'  # serve asset files in static/ at /static/

# bundle folders to register with the app
BUNDLES = {
    # backend.folder: url_prefix
    'backend.site': '/',
    'backend.auth': '/api/v1/auth',
    'backend.api': '/api/v1',
}


class BaseConfig(object):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'not-secret-key')  # FIXME
    STRICT_SLASHES = False

    ##########################################################################
    # session/cookies                                                        #
    ##########################################################################
    SESSION_PROTECTION = 'strong'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # SECURITY_TOKEN_MAX_AGE is fixed from time of token generation;
    # it does not update on refresh like a session timeout would. for that,
    # we set (the ironically named) PERMANENT_SESSION_LIFETIME
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    ##########################################################################
    # database                                                               #
    ##########################################################################
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##########################################################################
    # mail                                                                   #
    ##########################################################################
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = ('Flask API', 'noreply@example.com')  # FIXME

    ##########################################################################
    # security                                                               #
    ##########################################################################
    # NOTE: itsdangerous "salts" are not normal salts in the cryptographic
    # sense, see https://pythonhosted.org/itsdangerous/#the-salt
    SECURITY_PASSWORD_SALT = os.environ.get('FLASK_SECURITY_PASSWORD_SALT',
                                            'security-password-salt')


class ProdConfig(BaseConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    ENV = 'prod'
    DEBUG = False

    ##########################################################################
    # database                                                               #
    ##########################################################################
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pw@localhost/db_name'  # FIXME

    ##########################################################################
    # session/cookies                                                        #
    ##########################################################################
    SESSION_COOKIE_DOMAIN = 'www.example.com'  # FIXME
    SESSION_TYPE = 'null'  # FIXME


class DevConfig(BaseConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    ENV = 'dev'
    DEBUG = True
    # EXPLAIN_TEMPLATE_LOADING = True

    ##########################################################################
    # session/cookies                                                        #
    ##########################################################################
    SESSION_COOKIE_SECURE = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'flask_sessions'

    ##########################################################################
    # database                                                               #
    ##########################################################################
    DB_NAME = 'dev.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(PROJECT_ROOT, DB_NAME)
    # SQLALCHEMY_ECHO = True

    ##########################################################################
    # mail                                                                   #
    ##########################################################################
    MAIL_PORT = 1025  # MailHog
    MAIL_DEFAULT_SENDER = ('Flask API', 'noreply@localhost')

class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # :memory: