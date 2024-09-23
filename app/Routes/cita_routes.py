from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Models.cita import Cita
from app.Models.servicio import Servicio
from app.Models.estilista import Estilista
from app import db

bp = Blueprint('cita', __name__)

@bp.route('/cita')
def index():
    data = Cita.query.all()
    servicio = Servicio.query.all()
    estilista = Estilista.query.all()

    return render_template('citas/index.html', data=data, servicio=servicio, estilista=estilista)

@bp.route('/citas_usuarios')
def index_user():
    data = Cita.query.all()
    servicio = Servicio.query.all()
    estilista = Estilista.query.all()

    return render_template('citas/indesuser.html', data=data, servicio=servicio, estilista=estilista)

@bp.route('/add', methods=['GET', 'POST'])
def add():  
    if request.method == 'POST':
        servicio_id = request.form.get('servicio_id')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        cliente = request.form.get('cliente')
        estilista_id = request.form.get('estilista_id')
        
        if not all([servicio_id, fecha, hora, estilista_id]):
            return "Faltan campos en el formulario", 400

        servicio = Servicio.query.get(servicio_id)
        estilista = Estilista.query.get(estilista_id)
        
        new_Cita = Cita(fecha=fecha, hora=hora, estilista=estilista, cliente=cliente, estilista_id=estilista_id, servicio=servicio, servicio_id=servicio_id)
        
        db.session.add(new_Cita)
        db.session.commit()

        return redirect(url_for('cita.index_user'))
    
    data = Servicio.query.all()
    data1 = Estilista.query.all()

    return render_template('citas/add.html', data=data, data1=data1)


@bp.route('/edit/<int:idcita>', methods=['GET', 'POST'])
def edit(idcita):
    cita = Cita.query.get_or_404(idcita)

    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        cliente = request.form.get['cliente']
        servicio_id = request.form['servicio']
        estilista_id = request.form['estilista']

        # Verifica que el servicio_id y estilista_id no estén vacíos
        if not all([servicio_id, estilista_id]):
            flash('Faltan campos en el formulario', 'error')
            return redirect(url_for('cita.edit', idcita=idcita))

        cita.fecha = fecha
        cita.hora = hora
        cita.cliente = cliente
        cita.servicio_id = servicio_id
        cita.servicio = Servicio.query.get(servicio_id)
        cita.estilista_id = estilista_id
        cita.estilista = Estilista.query.get(estilista_id)

        db.session.commit()

        return redirect(url_for('cita.index'))

    servicios = Servicio.query.all()
    estilistas = Estilista.query.all()

    return render_template('citas/edit.html', cita=cita, servicios=servicios, estilistas=estilistas)



@bp.route('/delete/<int:idcita>')
def delete(idcita):
    cita = Cita.query.get_or_404(idcita)

    db.session.delete(cita)
    db.session.commit()

    flash('Cita eliminada correctamente.', 'success')
    return redirect(url_for('cita.index_user'))
