from app import db


class Estilista(db.Model):

    __tablename__ = 'estilista'
    idEstilista = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
   
    cita = db.relationship('Cita', back_populates='estilista')