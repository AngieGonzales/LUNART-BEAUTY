from flask import Blueprint, render_template, redirect, url_for, request
from app.Models.estilista import Estilista

bp = Blueprint('menu', __name__)

@bp.route('/add_estilista')
def add_estilista():
    return render_template('estilistas/add.html')

@bp.route('/catalogo')
def ruta_catalogo():
    return render_template('catalogo/index.html')

@bp.route('/inicio')
def ruta_inicio():
    return render_template('menu/index.html')


@bp.route('/disponibilidad')
def ruta_disponibilidad():
    return render_template('citas/index.html')

@bp.route('/perfil')
def ruta_perfil():
    return render_template('usuarios/index.html')




    





