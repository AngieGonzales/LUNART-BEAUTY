import os

    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/belleza'
class Config:
    USER = os.getenv('MYSQL_USER', 'root')
    PASSWORD = os.getenv('MYSQL_PASSWORD', 'FJcDicglwsuwxNJUoEyNIeeRZyDLpUKr')
    HOST = os.getenv('MYSQL_HOST', 'autorack.proxy.rlwy.net:')  # Aquí cambiamos localhost por 'db', el nombre del servicio
    PORT = os.getenv('MYSQL_PORT', 29344)
    DATABASE = os.getenv('MYSQL_DATABASE', 'belleza')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/belleza'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Configuración para la carga de imágenes
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'app/static/uploads'  # Carpeta donde se guardarán las imágenes subidas
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Tamaño máximo de archivo (16 MB)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas
    ADMIN_SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY') or 'admin123'

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

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'