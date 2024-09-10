from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.Models.servicio import Servicio

bp = Blueprint('servicio', __name__)

@bp.route('/servicio')
def index():
    data = Servicio.query.all()
    return render_template('servicios/index.html', data=data)



@bp.route('/servicio/add', methods=['GET', 'POST'])
def add():  

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        duracion = request.form['duracion']

        new_servicio = Servicio(nombre=nombre, precio = precio, duracion = duracion)
        db.session.add(new_servicio)
        db.session.commit()


        return redirect(url_for('servicio.index'))
    return render_template('servicios/add.html' )