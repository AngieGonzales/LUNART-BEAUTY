from flask import Blueprint, jsonify, request, render_template
from app.Models.carrito import Carrito
from app import db
import requests

bp = Blueprint('carrito', __name__) 

# Ruta para mostrar la página del carrito
@bp.route('/carrito')
def ruta_carrito():
    return render_template('carrito/index.html')


# Ruta para guardar los productos en el carrito
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


# Ruta para simular el pago
@bp.route('/api/pagar', methods=['POST'])
def pagar():
    data = request.json
    plataforma = data.get('plataforma')
    total = data.get('total')
    carrito = data.get('carrito')

    # Determina la URL de pago según la plataforma
    if plataforma == 'nequi':
        url_pago = "https://api.nequi.com/pago"  # URL ficticia
    elif plataforma == 'daviplata':
        url_pago = "https://api.daviplata.com/pago"  # URL ficticia
    elif plataforma == 'bancolombia':
        url_pago = "https://api.bancolombia.com/pago"  # URL ficticia
    else:
        return jsonify(success=False, message='Plataforma de pago no soportada'), 400

    # Simulando la llamada a la API de pago
    try:
        response = requests.post(url_pago, json={'total': total, 'carrito': carrito})
        
        if response.status_code == 200:
            return jsonify(success=True, url=response.json().get('url', ''))
        else:
            return jsonify(success=False, message='Error al procesar el pago'), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify(success=False, message='Error en la conexión: ' + str(e)), 500


# Ruta para generar la factura
@bp.route('/generar_factura', methods=['POST'])
def generar_factura():
    carrito_items = Carrito.query.all()  # Obtén todos los productos del carrito de la base de datos
    total = sum(item.subtotal for item in carrito_items)  # Calcula el total a pagar

    # Renderiza la plantilla de la factura y pasa los detalles del carrito y el total
    return render_template('carrito/factura.html', carrito_items=carrito_items, total=total)


if __name__ == '__main__':
    # Asegúrate de tener un archivo de Flask ejecutando la aplicación
    from app import app  # Importa tu aplicación Flask aquí
    app.register_blueprint(bp)  # Registra el blueprint
    app.run(debug=True)
