# = Holds configurations to be used in create_app() to configure app:

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Murphy324!!@localhost/mechanic_shop'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
# Test Configuration:
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass




