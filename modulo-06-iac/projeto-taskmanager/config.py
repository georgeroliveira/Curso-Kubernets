import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    PORT = int(os.getenv('PORT', '5000'))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

    try:
        with open('VERSION', 'r') as f:
            VERSION = f.read().strip()
    except:
        VERSION = '0.0.0'

config = Config()
