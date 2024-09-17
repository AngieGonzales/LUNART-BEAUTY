from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Models.estilista import Estilista
from app import db

bp = Blueprint('estilistas', __name__)

@bp.route('/estilista')
def index():
    dataE = Estilista.query.all()
    return render_template('estilistas/index.html' ,dataE=dataE)

@bp.route('/agregar-estilistas', methods=['GET', 'POST'])
def add():  
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        cargo = request.form['cargo']

        # Validar que no haya campos vacíos (opcional, pero recomendado)
        if not nombre or not telefono or not cargo:
            return redirect(url_for('estilistas.add'))

        # Crear nuevo estilista y guardar en la base de datos
        new_estilista = Estilista(nombre=nombre, telefono=telefono, cargo=cargo)
        db.session.add(new_estilista)
        db.session.commit()

        # Mensaje de éxito
        flash('Estilista agregado exitosamente.', 'success')

        # Redirigir al índice de estilistas
        return redirect(url_for('estilistas.add'))

    # Renderizar el formulario de adición
    return render_template('estilistas/add.html')

@bp.route('/estilista/edit/<int:idEstilista>', methods=['GET', 'POST'])
def edit(idEstilista):
    estilista = Estilista.query.get_or_404(idEstilista)

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        cargo = request.form['cargo']

        if not nombre or not telefono or not cargo:
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('estilistas.edit', idEstilista=idEstilista))

        estilista.nombre = nombre
        estilista.telefono = telefono
        estilista.cargo = cargo

        db.session.commit()
        flash('Estilista actualizado correctamente.', 'success')
        return redirect(url_for('estilistas.index'))
    
    return render_template('estilistas/edit.html', estilista=estilista)

@bp.route('/estilista/delete/<int:idEstilista>')
def delete(idEstilista):
    estilista = Estilista.query.get_or_404(idEstilista)

    db.session.delete(estilista)
    db.session.commit()

    flash('Estilista eliminado correctamente.', 'success')

    return redirect(url_for('estilistas.index'))
