from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import LoginManager
import os
from datetime import datetime
import locale

db = SQLAlchemy()
login_manager = LoginManager()
scheduler = BackgroundScheduler()

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

    from app.Routes import cita_routes
    app.register_blueprint(cita_routes.bp)

    with app.app_context():
        schedule_cita_cleanup()

    scheduler.start()


    from app.Routes import servicio_routes, menu_routes, estilista_routes, carrito_routes, usuario_routes,  producto_routes, categoria_routes, contacto_routes

    app.register_blueprint(servicio_routes.bp)
    app.register_blueprint(menu_routes.bp)
    app.register_blueprint(carrito_routes.bp)
    app.register_blueprint(estilista_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(producto_routes.bp)
    app.register_blueprint(categoria_routes.bp)
    app.register_blueprint(contacto_routes.bp)

    app.config['SQLALCHEMY_ECHO'] = True

    # Configurar la localización para el formato de números
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    # Registrar el filtro personalizado
    @app.template_filter('format_price')
    def format_price(value):
        return locale.format_string('%.2f', value, grouping=True)

    return app

def eliminar_citas_vencidas():
    with create_app().app_context():
        fecha_actual = datetime.now().date()
        citas_vencidas = Cita.query.filter(Cita.fecha < fecha_actual).all()
        for cita in citas_vencidas:
            db.session.delete(cita)
        db.session.commit()
        print(f"Se eliminaron {len(citas_vencidas)} citas vencidas.")

def schedule_cita_cleanup():
    scheduler.add_job(eliminar_citas_vencidas, 'interval', hours=24)