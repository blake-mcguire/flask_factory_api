import os



class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:#InnaGLEAMG43@localhost/advanced_api'
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    DEBUG = True


class ProductionConfig:
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite://app.db'
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    DEBUG = False