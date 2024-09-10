from app import db

class Servicio(db.Model):
    __tablename__='servicio'
    idservicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
   
    cita = db.relationship('Cita', back_populates='servicio')