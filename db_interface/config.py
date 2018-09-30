class Config(object):
    DEBUG = True
    SECRET_KEY = b'\xce\xa4\xb4 \xc4\x1e\x885\xfc>W\x01J\xff\xf3z'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
