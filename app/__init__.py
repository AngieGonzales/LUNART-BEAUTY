from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(cliente_idcliente):
        
        from .Models.cliente import Cliente
        return Cliente.query.get(cliente_idcliente)

    from app.Routes import cita_routes, servicio_routes, menu_routes, estilista_routes, carrito_routes

    app.register_blueprint(cita_routes.bp)
    app.register_blueprint(servicio_routes.bp)
    app.register_blueprint(menu_routes.bp)
    app.register_blueprint(carrito_routes.bp)
    app.register_blueprint(estilista_routes.bp)

    from app.Routes.auth import auth_bp
    app.register_blueprint (auth_bp)


    return app