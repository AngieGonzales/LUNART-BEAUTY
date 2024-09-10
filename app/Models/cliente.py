from app import db
from flask_login import UserMixin


class Cliente(db.Model, UserMixin):
    __tablename__='cliente'
    idcliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    passwordclien = db.Column(db.String(255), nullable=False)