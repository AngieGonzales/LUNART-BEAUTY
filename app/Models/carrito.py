from app import db

class Carrito(db.Model):
    __tablename__ = 'carrito'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.idproducto'), nullable=False)  # Clave foránea
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Relación con Producto
    producto = db.relationship('Producto', back_populates='carrito')  # Cambié aquí

    def __init__(self, producto_id, cantidad, precio):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio = precio
        self.subtotal = cantidad * precio
