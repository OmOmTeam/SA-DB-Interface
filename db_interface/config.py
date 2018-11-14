class Config(object):
    DEBUG = True
    SECRET_KEY = b'\xce\xa4\xb4 \xc4\x1e\x885\xfc>W\x01J\xff\xf3z'
    MYSQL_HOST = "10.90.138.29"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "SATeamDB777"
    JSON_AS_ASCII = False


class DevelopConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
