from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.Models.usuario import Usuario
from app import db
import datetime


bp = Blueprint('usuario', __name__)

@bp.route('/', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        celular = request.form.get('celular')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        fecha_registro = request.form.get('fecha_registro')

        if not nombre.isalpha() or not apellido.isalpha():
            flash('Nombre y apellido solo deben contener letras.')
            return redirect(url_for('usuario.registro'))
        if len(celular) != 10 or not celular.isdigit():
            flash('El celular debe tener 10 dígitos.')
            return redirect(url_for('usuario.registro'))
        if '@' not in correo:
            flash('El correo debe contener un @.')
            return redirect(url_for('usuario.registro'))
        if len(contraseña) <= 5:
            flash('La contraseña debe tener más de 5 caracteres.')
            return redirect(url_for('usuario.registro'))
        try:
            datetime.strptime(fecha_registro, '%d/%m/%y')
        except ValueError:
            flash('La fecha debe estar en formato DD/MM/AA.')
            return redirect(url_for('usuario.registro'))
        if not nombre or not apellido or not celular or not correo or not contraseña or not rol:
            flash('No puede haber campos vacíos.')
            return redirect(url_for('usuario.registro'))

    
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            celular=celular,
            correo=correo,
            rol=rol,
            fecha_registro=datetime.strptime(fecha_registro, '%d/%m/%y')
        )
        nuevo_usuario.set_password(contraseña)  
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado con éxito.')
        return redirect(url_for('auth.login'))  


    return render_template('registro/registrar.html')