class Config(object):
    DEBUG = True
    SECRET_KEY = b'\xce\xa4\xb4 \xc4\x1e\x885\xfc>W\x01J\xff\xf3z'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:SATeamDB777@10.90.138.29:6033/'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_HOST = "10.90.138.29"
    MYSQL_PORT = 6033
    # MYSQL_PORT = 3066
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "SATeamDB777"
    JSON_AS_ASCII = False


class DevelopConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
