# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = True

