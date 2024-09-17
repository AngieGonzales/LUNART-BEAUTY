from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.Models.servicio import Servicio

bp = Blueprint('servicio', __name__)

@bp.route('/servicio')
def index():
    data = Servicio.query.all()
    return render_template('servicios/index.html', data=data)

@bp.route('/servicioadmin')
def index_admin():
    data = Servicio.query.all()
    return render_template('servicios/indexadmin.html', data=data)

@bp.route('/servicio/add', methods=['GET', 'POST'])
def add():  

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']

        new_servicio = Servicio(nombre=nombre, precio = precio)
        db.session.add(new_servicio)
        db.session.commit()


        return redirect(url_for('servicio.index_admin'))
    return render_template('servicios/add.html' )

@bp.route('/servicio/edit/<int:idservicio>', methods=['GET', 'POST'])
def edit(idservicio):
    servicio = Servicio.query.get_or_404(idservicio)

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']

        if not nombre or not precio:
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('servicio.edit', idservicio=idservicio))

        servicio.nombre = nombre
        servicio.precio = precio

        db.session.commit()
        flash('Servicio actualizado correctamente.', 'success')
        return redirect(url_for('servicio.index_admin'))
    
    return render_template('servicios/editadmin.html', servicio=servicio)

@bp.route('/servicio/delete/<int:idservicio>')
def delete(idservicio):

    servicio = Servicio.query.get_or_404(idservicio)

    db.session.delete(servicio)
    db.session.commit()

    flash('Servicio eliminado correctamente.', 'success')

    return redirect(url_for('servicio.index_admin'))