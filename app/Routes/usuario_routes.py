from flask import Blueprint, render_template, request, redirect, url_for, flash, session, logging
from app.Models.usuario import Usuario
from app import db
from datetime import date


bp = Blueprint('usuario', __name__)

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        celular = request.form.get('celular')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        fecha_nacimiento = request.form.get('fecha_nacimiento')

        if not nombre.replace(" ", "").isalpha() or not apellido.replace(" ", "").isalpha():
            print(f"Alfa Nombre {nombre} alfaapellido {apellido} ")

            print(f"Alfa Nombre {nombre.isalpha()} alfaapellido {apellido.isalpha()} ")
            flash('NOMBRE Y APELLIDO SOLO DEBEN CONTENER LETRAS.')
            return redirect(url_for('usuario.registro'))
        
        if len(celular) != 10 or not celular.isdigit():
            flash('EL CELULAR DEBE TENER 10 DIGITOS.')
            return redirect(url_for('usuario.registro'))
        
        if '@' not in correo:
            flash('EL CORREO DEBE CONTENER UN @.')
            return redirect(url_for('usuario.registro'))
        
        if len(contraseña) <= 4:
            flash('LA CONTRASEÑA DEBE CONTENER MAS DE 4 CARACTERES.')
            return redirect(url_for('usuario.registro'))
        
        try:
          fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
        except ValueError:
            flash('LA FECHA DEBE ESTAR EN FORMATO DD/MM/AAAA.')
            return redirect(url_for('usuario.registro'))

        
        if not nombre or not apellido or not celular or not correo or not contraseña or not rol:
            flash('NO PUEDEN HABER CAMPOS VACIOS.')
            return redirect(url_for('usuario.registro'))

       
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            celular=celular,
            correo=correo,
            rol=rol,
            fecha_nacimiento=fecha_nacimiento  
        )
        
        # Hash de la contraseña
        nuevo_usuario.set_password(contraseña)
        
        try:
            print("En el try")
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado con éxito.')
            return redirect(url_for('usuario.login'))
        except Exception as e:           
            db.session.rollback() # Deshacer los cambios si ocurre un error
            logging.error(f"Error al registrar el usuario: {str(e)}")  # Registrar el error
            flash(f'Error al registrar el usuario: {str(e)}')
            return redirect(url_for('usuario.registro'))

    return render_template('registro/registrar.html')


@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario is None:
            flash('Por favor registrate antes de iniciar sesión')
            return redirect(url_for('usuario.login'))
        
        if usuario and usuario.check_password(contraseña):
            session['usuario_id'] = usuario.id  # Guardar ID del usuario en la sesión
            session['rol'] = usuario.rol  # Guardar el rol en la sesión

            # Redirigir según el rol
            if usuario.rol == 'Administrador':
                return redirect(url_for('usuario.admin_dashboard'))  # Redirigir al panel de administración
            else:
                return redirect(url_for('usuario.index'))  # Redirigir a la página de usuario
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('usuario.login'))

    return render_template('registro/login.html')

@bp.route('/logout')
def logout():
    session.clear()  # Limpiar la sesión
    flash('Sesión cerrada.')
    return redirect(url_for('usuario.login'))

@bp.route('/home')
def index():
    return render_template('menu/index.html')  # Página de inicio para el usuario normal

# Ruta del administrador
@bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')  # Panel de administración
    

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Obtener el usuario por ID
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        celular = request.form.get('celular')

        # Actualizar los campos del usuario
        usuario.nombre = nombre
        usuario.correo = correo
        usuario.celular = celular

        try:
            # Guardar cambios en la base de datos
            db.session.commit()
            flash('Perfil actualizado con éxito.')
            return redirect(url_for('usuario.index'))  # Cambia esto a la ruta correcta
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}')

    # Renderizar el formulario para editar, pasando 'usuario'
    return render_template('usuario/edit.html', usuario=usuario)
