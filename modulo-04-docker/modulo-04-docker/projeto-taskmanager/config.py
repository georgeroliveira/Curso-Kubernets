class BaseConfig:
    VERSION = "0.2.0"
    ENVIRONMENT = "development"
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENVIRONMENT = "production"

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config(env="development"):
    return config_map.get(env, DevelopmentConfig)
