from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.Models import Contacto  
from app import db

bp = Blueprint('contact', __name__)

@bp.route('/enviar_contacto', methods=['POST'])
def enviar_contacto():
    if request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']

        # Crea una nueva instancia del modelo contacto
        nuevo_contacto = Contacto(phone=phone, email=email, message=message)

        try:
            # Agrega el nuevo contacto a la base de datos
            db.session.add(nuevo_contacto)
            db.session.commit()
            flash('Mensaje enviado correctamente')
            return redirect(url_for('menu.ruta_contacto'))
        except Exception as e:
            db.session.rollback() # Si algo sale mal revierte la transaccion
            flash('Error al enviar el mensaje.Intenta de nuevo')
            print(e)
            return redirect(url_for('menu.ruta_contacto'))