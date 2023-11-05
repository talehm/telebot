class Config:
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/telegram"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my-secret-key"
