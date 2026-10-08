import os


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    CACHE_TYPE = "SimpleCache"
    RATELIMIT_ENABLED = False


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = os.environ.get("SECRET_KEY")