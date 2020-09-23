class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/focusplus'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']