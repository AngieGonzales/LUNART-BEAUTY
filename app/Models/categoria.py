from app import db

class Categoria(db.Model):
    idCategoria = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre= db.Column(db.String(255), nullable=False)
    descripcion= db.Column(db.String(255), nullable=False) 
    imagen=db.Column(db.String(255), nullable=False)

    productoss = db.relationship("Producto", back_populates="categorias")

