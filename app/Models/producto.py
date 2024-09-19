from app import db


class Producto(db.Model):
    __tablename__='producto'
    idproducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.String(255), nullable=False)
    imagen=db.Column(db.String(255), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'))

    categorias = db.relationship("Categoria", back_populates="productoss")
    
