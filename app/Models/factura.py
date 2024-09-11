from app import db
from datetime import datetime


class Factura(db.Model):
    __tablename__='factura'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)


    