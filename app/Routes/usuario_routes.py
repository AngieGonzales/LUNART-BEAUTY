from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Models.usuario import Usuario
from app import db
from datetime import date



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
        fecha_nacimiento = request.form.get('fecha_nacimiento')

        # Validaciones del formulario
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

        # Formato correcto de fecha: AAAA-MM-DD
        try:
          fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
        except ValueError:
            flash('La fecha debe estar en formato AAAA-MM-DD.')
            return redirect(url_for('usuario.registro'))

        # Validación de campos vacíos
        if not nombre or not apellido or not celular or not correo or not contraseña or not rol:
            flash('No puede haber campos vacíos.')
            return redirect(url_for('usuario.registro'))

        # Creación del nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            celular=celular,
            correo=correo,
            rol=rol,
            fecha_nacimiento=fecha_nacimiento  # Ya está en el formato correcto
        )
        
        # Hash de la contraseña
        nuevo_usuario.set_password(contraseña)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado con éxito.')
            return redirect(url_for('usuario.login'))
        except Exception as e:
            db.session.rollback()  # Deshacer los cambios si ocurre un error
            flash(f'Error al registrar el usuario: {str(e)}')
            return redirect(url_for('usuario.registro'))

    return render_template('registro/registrar.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario and usuario.check_password(contraseña):
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('usuario.registro'))
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('usuario.login'))

    return render_template('registro/login.html')
