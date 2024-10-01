from app import create_app, db
import pytest

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        #db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def usuario(app):
    from app.Models import Usuario
    usuario = Usuario(username='test_user', password='test_password')
    db.session.add(usuario)
    db.session.commit()
    yield usuario
    db.session.delete(usuario)
    db.session.commit()

