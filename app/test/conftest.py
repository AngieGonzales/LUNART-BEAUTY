from app import create_app, db, scheduler
import pytest

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        #db.drop_all()

    scheduler.shutdown()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def usuario(app):
    from app.Models import Usuario
    usuario = Usuario(nombre='test_user', apellido='test_apellido', celular='1234567890', correo='test@test.com', password_hash='test_password', fecha_nacimiento='2000-01-01', rol='admin')
    db.session.add(usuario)
    db.session.commit()
    yield usuario
    db.session.delete(usuario)
    db.session.commit()

