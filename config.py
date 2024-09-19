import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/belleza'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Configuración para la carga de imágenes
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'app/static/uploads'  # Carpeta donde se guardarán las imágenes subidas
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Tamaño máximo de archivo (16 MB)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas

    @staticmethod
    def init_app(app):
        pass

# Opcionalmente, puedes crear otras configuraciones (development, testing, production) si es necesario
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
