
from app import db 

class Carrito(db.Model):
    __tablename__='carrito'
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)


    