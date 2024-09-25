from flask import Blueprint, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from app.Models.carrito import Carrito
  # Asegúrate de tener este modelo
from app import db

bp = Blueprint('carrito', __name__)

# Ruta para mostrar la página del carrito
@bp.route('/carrito')
def ruta_carrito():
    return render_template('carrito/index.html')

# Ruta para guardar el carrito
@bp.route('/guardar_carrito', methods=['POST'])
def guardar_carrito():
    data = request.json
    carrito_items = data.get('carrito')  # Asegúrate de que el JSON contenga una clave 'carrito'

    if carrito_items:
        for item in carrito_items:
            # Validación simple
            if not all(key in item for key in ['producto', 'cantidad', 'precio']):
                return jsonify({"message": "Datos incompletos en el carrito"}), 400
            
            if item['cantidad'] <= 0 or item['precio'] < 0:
                return jsonify({"message": "Cantidad y precio deben ser mayores que cero"}), 400

            # Cambia esta línea para usar producto_id
            nuevo_item = Carrito(
                producto_id=item['producto'],  # Asegúrate de usar el ID del producto
                cantidad=item['cantidad'],
                precio=item['precio'],
                subtotal=item['cantidad'] * item['precio'],
            )
            db.session.add(nuevo_item)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Revertir cambios en caso de error
            return jsonify({"message": str(e)}), 500  # Retorna el error

    return jsonify({"message": "Carrito guardado exitosamente"}), 201

# Ruta para guardar la factura
@bp.route('/guardar_factura', methods=['POST'])
def guardar_factura():
    try:
        data = request.get_json()
        total = data.get('total')
        carrito = data.get('carrito')

        for item in carrito:
            nueva_factura = Factura(
                producto_id=item.get('producto'),  # Asegúrate de que tu objeto tenga el id del producto
                cantidad=item['cantidad'],
                precio=item['precio'],
                subtotal=item['cantidad'] * item['precio'],
                total=total
            )
            db.session.add(nueva_factura)

        db.session.commit()
        return jsonify({'message': 'Factura guardada exitosamente!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
