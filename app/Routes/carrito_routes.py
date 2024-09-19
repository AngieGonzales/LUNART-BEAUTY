from flask import Blueprint, jsonify, request
from app.Models.carrito import Carrito
from app import db

bp = Blueprint('carrito', __name__)

@bp.route('/guardar_carrito', methods=['POST'])
def guardar_carrito():
    data = request.json  # Obtén los datos enviados desde el frontend
    carrito_items = data.get('carrito')

    if carrito_items:
        for item in carrito_items:
            nuevo_item = Carrito(
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio=item['precio'],
                subtotal=item['cantidad'] * item['precio'],
                
            )
            db.session.add(nuevo_item)
        db.session.commit()

    return jsonify({"message": "Carrito guardado exitosamente"}), 201

