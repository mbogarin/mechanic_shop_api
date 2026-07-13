import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Murphy324!!@localhost/mechanic_shop"
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
# Test Configuration:
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = "SimpleCache"




