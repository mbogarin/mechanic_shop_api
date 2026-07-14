import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVELOPMENT_DATABASE_URI",
        "sqlite:///development.db" 
        )
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = "SimpleCache"




