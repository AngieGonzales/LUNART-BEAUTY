from app import db


class Registro(db.Model):
    __tablename__='registro'
    idregistro = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.String(255), nullable=False)

    producto =  db.Column(db.Integer, db.ForeignKey('producto.idproducto'))





    