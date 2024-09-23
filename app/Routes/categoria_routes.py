import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app.Models.categoria import Categoria
from app import db

bp = Blueprint('categoria', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/categoria/admin')
def index():
    # Corregido: uso de query.all() para obtener todas las categorías
    data = Categoria.query.all()
    return render_template('categoria/index.html', data=data)

@bp.route('/categoria/index_cliente')
def index_cliente():
    db.session.remove()
    data = Categoria.query.all()
    return render_template('categoria/index_cliente.html', data=data)

@bp.route('/categoria/add', methods=['GET', 'POST'])
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

            # Se crea la nueva categoría y se guarda en la base de datos
            new_categoria = Categoria(nombre=nombre, descripcion=descripcion, imagen=filename)
            db.session.add(new_categoria)
            db.session.commit()

            return redirect(url_for('categoria.index'))

    return render_template('categoria/add.html')

@bp.route('/categoria/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        categoria.descripcion = request.form['descripcion']

        # Solo actualiza la imagen si el usuario sube una nueva
        if 'imagen' in request.files and request.files['imagen'].filename != '':
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                categoria.imagen = filename

        db.session.commit()
        return redirect(url_for('categoria.index'))

    return render_template('categoria/edit.html', categoria=categoria)

@bp.route('/categoria/delete/<int:id>')
def delete(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()

    return redirect(url_for('categoria.index'))
