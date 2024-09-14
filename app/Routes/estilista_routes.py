from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Models.estilista import Estilista
from app import db

bp = Blueprint('estilistas', __name__)

@bp.route('/estilista')
def index():
    # Obtener todos los estilistas de la base de datos
    data = Estilista.query.all()
    
    # Renderizar la plantilla con los estilistas
    return render_template('estilistas/index.html', data=data)

@bp.route('/add', methods=['GET', 'POST'])
def add():  
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        cargo = request.form['cargo']

        # Validar que no haya campos vacíos (opcional, pero recomendado)
        if not nombre or not telefono or not cargo:
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('estilistas.add'))

        # Crear nuevo estilista y guardar en la base de datos
        new_estilista = Estilista(nombre=nombre, telefono=telefono, cargo=cargo)
        db.session.add(new_estilista)
        db.session.commit()

        # Mensaje de éxito
        flash('Estilista agregado exitosamente.', 'success')

        # Redirigir al índice de estilistas
        return redirect(url_for('estilistas.index'))

    # Renderizar el formulario de adición
    return render_template('estilistas/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Obtener el estilista por ID, si no se encuentra, retorna un error 404
    estilista = Estilista.query.get_or_404(id)

    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        cargo = request.form['cargo']

        # Validar los campos
        if not nombre or not telefono or not cargo:
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('estilistas.edit', id=id))

        # Actualizar los valores del estilista
        estilista.nombre = nombre
        estilista.telefono = telefono
        estilista.cargo = cargo

        # Guardar los cambios en la base de datos
        db.session.commit()

        # Mensaje de éxito
        flash('Estilista actualizado correctamente.', 'success')

        # Redirigir al índice de estilistas tras la edición exitosa
        return redirect(url_for('estilistas.index'))

    # Renderizar el formulario de edición con los datos actuales del estilista
    return render_template('estilistas/edit.html', estilista=estilista)

@bp.route('/delete/<int:id>')
def delete(id):
    # Obtener el estilista por ID, si no se encuentra, retorna un error 404
    estilista = Estilista.query.get_or_404(id)

    # Eliminar el estilista de la base de datos
    db.session.delete(estilista)
    db.session.commit()

    # Mostrar un mensaje de éxito
    flash('Estilista eliminado correctamente.', 'success')

    # Redirigir al índice de estilistas tras la eliminación exitosa
    return redirect(url_for('estilistas.index'))
