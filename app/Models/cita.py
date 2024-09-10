from app import db

class Cita(db.Model):
    __tablename__='cita'
    idcita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    estilista = db.Column(db.String(255), nullable=False)
    servicio_id = db.Column(db.Integer,  db.ForeignKey('servicio.idservicio'),nullable = True)
    estilista_id = db.Column(db.Integer,  db.ForeignKey('estilista.idEstilista'),nullable = True)
  
    servicio = db.relationship("Servicio", back_populates="cita")
    estilista= db.relationship("Estilista", back_populates="cita")


    
    
    


