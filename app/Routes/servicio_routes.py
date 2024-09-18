from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.Models.servicio import Servicio
import os
from werkzeug.utils import secure_filename

bp = Blueprint('servicio', __name__)


@bp.route('/servicio')
def index():
    data = Servicio.query.all()
    return render_template('servicios/index.html', data=data)

@bp.route('/servicioadmin')
def index_admin():
    data = Servicio.query.all()
    return render_template('servicios/indexadmin.html', data=data)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/servicio/add', methods=['GET', 'POST'])
def add():  

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        if 'imagen' not in request.files:
            return "No se ha seleccionado ninguna imagen", 400
        
        file = request.files['imagen']
        if file.filename == '':
            return "Nombre de archivo vacío", 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)


        new_servicio = Servicio(nombre=nombre, descripcion=descripcion, imagen=filename)
        db.session.add(new_servicio)
        db.session.commit()

        return redirect(url_for('servicio.index_admin'))
    return render_template('servicios/add.html' )

@bp.route('/servicio/edit/<int:idservicio>', methods=['GET', 'POST'])
def edit(idservicio):
    servicio = Servicio.query.get_or_404(idservicio)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        if 'imagen' in request.files and request.files['imagen'].filename != '':
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                servicio.imagen = filename

        if not nombre or not descripcion:
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('servicio.edit', idservicio=idservicio))

        servicio.nombre = nombre
        servicio.descripcion = descripcion

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