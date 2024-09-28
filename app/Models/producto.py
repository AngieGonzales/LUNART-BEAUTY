from app import db


class Producto(db.Model):
    __tablename__='producto'
    idproducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)  # Cambiado a Float
    imagen=db.Column(db.String(255), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'))
    stock = db.Column(db.Integer, default=0)

    categorias = db.relationship("Categoria", back_populates="productoss")
    carritos = db.relationship('Carrito', back_populates='producto')

    
