from app import db
from datetime import datetime

class Cita(db.Model):
    __tablename__='cita'
    idcita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    cliente = db.Column(db.String(50), nullable=False)
    servicio_id = db.Column(db.Integer,  db.ForeignKey('servicio.idservicio'),nullable = True)
    estilista_id = db.Column(db.Integer,  db.ForeignKey('estilista.idEstilista'),nullable = True)
  
    servicio = db.relationship("Servicio", back_populates="cita")
    estilista= db.relationship("Estilista", back_populates="cita")

    def __init__(self, fecha, hora, cliente, servicio_id, estilista_id, servicio, estilista):
        self.fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        self.hora = datetime.strptime(hora, '%H:%M').time()
        self.cliente = cliente
        self.servicio_id = servicio_id
        self.estilista_id = estilista_id
        self.servicio = servicio
        self.estilista = estilista

    
    
    


