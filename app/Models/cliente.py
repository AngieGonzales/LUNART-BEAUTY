from app import db
from flask_login import UserMixin


class Cliente(db.Model, UserMixin):
    __tablename__='cliente'
    idcliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    passwordclien = db.Column(db.String(255), nullable=False)



    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.idcliente)