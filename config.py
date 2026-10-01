class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    CACHE_TYPE = "SimpleCache"
    RATELIMIT_ENABLED = False