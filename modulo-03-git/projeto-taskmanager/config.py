import os

class Config:
    """Configuracao base do TaskManager"""
    
    # Aplicacao
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Servidor
    PORT = int(os.getenv('PORT', '5000'))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Ambiente
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Versao - lida do arquivo VERSION
    try:
        with open('VERSION', 'r') as f:
            VERSION = f.read().strip()
    except:
        VERSION = '0.1.0'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Health Check
    HEALTH_CHECK_TIMEOUT = int(os.getenv('HEALTH_CHECK_TIMEOUT', '30'))

class DevelopmentConfig(Config):
    """Configuracoes especificas de desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuracoes especificas de producao"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Seguranca em producao
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# Mapeamento de ambientes
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuracao baseada no ambiente atual"""
    env = os.getenv('ENVIRONMENT', 'development')
    return config_map.get(env, config_map['default'])