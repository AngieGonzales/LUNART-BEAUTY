from app import db
from sqlalchemy.orm import relationship

class Compra(db.Model):
    __tablename__='compra'
    idcompra= db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.Date, nullable = False)
    total = db.Column(db.Float, nullable =False)

    provedor = db.Column(db.Integer, db.ForeignKey('provedor.idprovedor'))
    empleado =  db.Column(db.Integer, db.ForeignKey('empleado.idempleado'))