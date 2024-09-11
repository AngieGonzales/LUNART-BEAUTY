from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('menu', __name__)

@bp.route('/estilista')

def index():
    return render_template('estilista/index.html')


@bp.route('/catalogo')

def ruta_catalogo():
    return render_template('catalogo/index.html')

@bp.route('/contacto')
def ruta_contacto():
    return render_template('contacto/index.html')


@bp.route('/servicios')
def ruta_servicios():
    return render_template('servicios/index.html')


@bp.route('/citas')

def ruta_citas():
    return redirect(url_for('cita.add'))


@bp.route('/inicio')

def ruta_inicio():
    return render_template('menu/index.html')



@bp.route('/disponibilidad')
def ruta_disponibilidad():
    return render_template('citas/index.html')



@bp.route('/carrito')
def ruta_carrito():
    return render_template('carrito/index.html')


@bp.route('/catalogo/esmaltes')
def ruta_esmaltes():
    return render_template('catalogo/esmalte.html')



@bp.route('/catalogo/exfoliante')
def ruta_exfoliante():
    return render_template('catalogo/exfoliante.html')



@bp.route('/catalogo/aceites')
def ruta_aceites():
    return render_template('catalogo/aceites.html')


@bp.route('/catalogo/shampos')
def ruta_shampos():
    return render_template('catalogo/shampos.html')



@bp.route('/catalogo/tratamientos')
def ruta_tratamientos():
    return render_template('catalogo/tratamientos.html')


@bp.route('/catalogo/tintes')
def ruta_tintes():
    return render_template('catalogo/tintes.html')


@bp.route('/catalogo/cera')
def ruta_cera():
    return render_template('catalogo/cera.html')


