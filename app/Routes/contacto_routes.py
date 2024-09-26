from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.Models import Contacto  
from app import db

bp = Blueprint('contact', __name__)

@bp.route('/enviar_contacto', methods=['GET', 'POST'])
def enviar_contacto():
    if request.method == 'POST':
        message = request.form.get('message')

        # Crea una nueva instancia del modelo contacto
        nuevo_comentario = Contacto(message=message)

        try:
            # Agrega el nuevo contacto a la base de datos
            db.session.add(nuevo_comentario)
            db.session.commit()
            flash('Mensaje enviado correctamente', 'success')
            return redirect(url_for('contact.enviar_contacto')) # Redirijir al mismo formulario
            
        except Exception as e:
            db.session.rollback() # Si algo sale mal revierte la transaccion
            flash('Error al enviar el mensaje.Intenta de nuevo', 'danger')
            print(e)
            return redirect(url_for('contact.enviar_contacto')) #Redirige de nuevo al mismo formulario
    #Si el metodo es get, simplemente muestra el formulario
    return render_template('contacto/index.html')
