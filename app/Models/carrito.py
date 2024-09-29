from app import db

class Carrito(db.Model):
    __tablename__ = 'carrito'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.idproducto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto', back_populates='carrito')
    usuario = db.relationship('Usuario', back_populates='carrito')

    def __init__(self, usuario_id, producto_id, cantidad, precio):
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio = precio
        self.subtotal = cantidad * precio
