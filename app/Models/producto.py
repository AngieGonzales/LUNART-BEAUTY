from app import db


class Producto(db.Model):
    __tablename__='producto'
    idproducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.String(255), nullable=False)
    
