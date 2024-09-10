from app import db


class Provedor(db.Model):
    __tablename__='provedor'
    idprovedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)

   