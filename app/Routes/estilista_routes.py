from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Models.estilista import Estilista
from app.Models.servicio import Servicio
from app import db

bp = Blueprint('estilistas', __name__)

@bp.route('/estilista')
def index():
    dataE = Estilista.query.all()
    return render_template('estilistas/index.html' ,dataE=dataE)

@bp.route('/agregar-estilistas', methods=['GET', 'POST'])
def add():  
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']


        if not nombre or not telefono:
            return redirect(url_for('estilistas.add'))
        

        new_estilista = Estilista(nombre=nombre, telefono=telefono)
        db.session.add(new_estilista)
        db.session.commit()

        return redirect(url_for('estilistas.index'))
    

    return render_template('estilistas/add.html')

@bp.route('/estilista/edit/<int:idEstilista>', methods=['GET', 'POST'])
def edit(idEstilista):
    estilista = Estilista.query.get_or_404(idEstilista)

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']

        if not nombre or not telefono:
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('estilistas.edit', idEstilista=idEstilista))

        estilista.nombre = nombre
        estilista.telefono = telefono

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
