import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app.Models.producto import Producto
from app.Models.categoria import Categoria
from app import db
from decimal import Decimal

bp = Blueprint('producto', __name__, url_prefix='/producto')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
@bp.route('/')
def indexproductos():
    productos = Producto.query.all()
    productos_bajo_stock = [p for p in productos if p.stock < 5]
    return render_template('producto/index.html', data=productos, productos_bajo_stock=productos_bajo_stock)

@bp.route('/<int:id>')
def index(id):
    data = Categoria.query.get_or_404(id)
    productos = data.productoss
    return render_template('producto/index.html', data=productos)

@bp.route('/index_cliente/<int:id>')
def index_cliente(id):
    data = Categoria.query.get_or_404(id)
    productos = data.productoss
    return render_template('producto/index_cliente.html', data=productos)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria'] 
        stock = request.form['stock']

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

            # Crear el nuevo producto incluyendo la categoría seleccionada
            new_producto = Producto(nombre=nombre, precio=precio, imagen=filename, categoria_id=categoria_id, stock=stock)
            db.session.add(new_producto)
            db.session.commit() 

            # Redirigir al índice del cliente con el 'id' de la categoría
            return redirect(url_for('producto.index', id=categoria_id))

    categorias = Categoria.query.all()
    return render_template('producto/add.html', categorias=categorias)
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        
        # Convertir el precio de string a Decimal
        precio_str = request.form.get('precio').replace('.', '').replace(',', '.')
        producto.precio = Decimal(precio_str)
        
        producto.categoria_id = request.form.get('categoria')
        producto.stock = request.form.get('stock')

        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                if producto.imagen:
                    old_image_path = os.path.join(upload_folder, producto.imagen)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                file.save(os.path.join(upload_folder, filename))
                producto.imagen = filename

        db.session.commit()
        # Redirigir al índice del cliente con el 'id' de la categoría
        return redirect(url_for('producto.index', id=producto.categoria_id))

    categorias = Categoria.query.all()
    return render_template('producto/edit.html', producto=producto, categorias=categorias)

@bp.route('/delete/<int:id>')
def delete(id):
    producto = Producto.query.get_or_404(id)
    categoria_id = producto.categoria_id  # Guardamos la categoría antes de eliminar el producto
    db.session.delete(producto)
    db.session.commit()

    # Redirigir al índice del cliente con el 'id' de la categoría
    return redirect(url_for('producto.index', id=categoria_id))
