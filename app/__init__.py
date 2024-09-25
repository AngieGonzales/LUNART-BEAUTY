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

    from app.Models.usuario import Usuario
    # Definir user_loader
    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

    from app.Routes import cita_routes, servicio_routes, menu_routes, estilista_routes, carrito_routes, usuario_routes,  producto_routes, categoria_routes
    from app.Routes import cita_routes, servicio_routes, menu_routes, estilista_routes, carrito_routes, usuario_routes, contacto_routes

    app.register_blueprint(cita_routes.bp)
    app.register_blueprint(servicio_routes.bp)
    app.register_blueprint(menu_routes.bp)
    app.register_blueprint(carrito_routes.bp)
    app.register_blueprint(estilista_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(producto_routes.bp)
    app.register_blueprint(categoria_routes.bp)
    app.register_blueprint(contacto_routes)
   
    

    app.register_blueprint(contacto_routes.bp)


    return app