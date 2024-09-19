from app import db

class Contacto(db.Model):
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)

    