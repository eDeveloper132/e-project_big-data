import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    DEBUG = False
    TESTING = False
    # In a real app, use a proper MongoDB URI
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/earthscape')
    # HDFS connection details
    HDFS_URL = os.environ.get('HDFS_URL', 'http://localhost:9870')
    HDFS_USER = os.environ.get('HDFS_USER', 'hadoop')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/earthscape_test'


class ProductionConfig(Config):
    """Production configuration."""
    # Production-specific settings
    pass

# Dictionary to access config classes by name
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
