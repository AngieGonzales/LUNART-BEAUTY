from flask import Blueprint, render_template, request, redirect, url_for
from app.Models.estilista import Estilista
from app import db
bp = Blueprint('estilistas', __name__)


@bp.route('/estilista')
def index():
    data = Estilista.query.all()
    
    return render_template('estilistas/index.html', data=data)




@bp.route('/add3', methods=['GET', 'POST'])
def add():  

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        cargo = request.form['cargo']


        new_estilista = Estilista(nombre=nombre, telefono = telefono, cargo = cargo)
        db.session.add(new_estilista)
        db.session.commit()


        return redirect(url_for('estilista.index'))
    return render_template('estilistas/add.html' )