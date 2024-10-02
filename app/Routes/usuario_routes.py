from flask import Blueprint, render_template, request, redirect, url_for, flash, session, logging, current_app
from app.Models.usuario import Usuario
from app import db
from datetime import date


bp = Blueprint('usuario', __name__)



@bp.route('/lista_usuarios')  
def lista_usuarios():
    data = Usuario.query.all()
    return render_template('usuarios/lista_usuarios.html', data=data)



@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        celular = request.form.get('celular')
        correo = request.form.get('correo')
        rol = request.form.get('rol')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        
        if rol == 'Administrador':
            admin_key = request.form.get('admin_key')
            if not admin_key:
                flash('Se requiere la clave de administrador.')
                return redirect(url_for('usuario.registro'))
            if admin_key != current_app.config['ADMIN_SECRET_KEY']:
                flash('Clave de administrador incorrecta.')
                return redirect(url_for('usuario.registro'))
            contraseña = admin_key  # Usa la clave de administrador como contraseña
        else:
            contraseña = request.form.get('contraseña')
            if not contraseña or len(contraseña) <= 4:
                flash('LA CONTRASEÑA DEBE CONTENER MAS DE 4 CARACTERES.')
                return redirect(url_for('usuario.registro'))

        if not nombre.replace(" ", "").isalpha() or not apellido.replace(" ", "").isalpha():
            flash('NOMBRE Y APELLIDO SOLO DEBEN CONTENER LETRAS.')
            return redirect(url_for('usuario.registro'))
        
        if len(celular) != 10 or not celular.isdigit():
            flash('EL CELULAR DEBE TENER 10 DIGITOS.')
            return redirect(url_for('usuario.registro'))
        
        if '@' not in correo:
            flash('EL CORREO DEBE CONTENER UN @.')
            return redirect(url_for('usuario.registro'))
        
        try:
          fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
        except ValueError:
            flash('LA FECHA DEBE ESTAR EN FORMATO DD/MM/AAAA Y SEPARAD POR /')
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
        
        nuevo_usuario.set_password(contraseña)
        
        try:
            print("Intentando guardar usuario en la base de datos...")
            db.session.add(nuevo_usuario)
            db.session.commit()
            print("Usuario registrado exitosamente.")
            flash('Usuario registrado con éxito.')
            return redirect(url_for('usuario.login'))
        except Exception as e:
            db.session.rollback()  
            logging.error(f"Error al registrar el usuario: {str(e)}")  
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
            flash('Por favor regístrate antes de iniciar sesión')
            return redirect(url_for('usuario.login'))
        
        if usuario and usuario.check_password(contraseña):
            session['usuario_id'] = usuario.id  
            session['rol'] = usuario.rol 

            
            if usuario.rol == 'Administrador':
                return redirect(url_for('usuario.admin_dashboard'))  
            else:
                return redirect(url_for('usuario.index'))  
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('usuario.login'))

    return render_template('registro/login.html')


@bp.route('/logout')
def logout():
    session.clear() 
    flash('Sesión cerrada.')
    return redirect(url_for('usuario.login'))

@bp.route('/home')
def index():
    return render_template('menu/index.html') 


@bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')  


    
@bp.route('/usuario/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        celular = request.form.get('celular')

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.celular = celular

        try:
            db.session.commit()
            flash('Perfil actualizado con éxito.')
            return redirect(url_for('usuario.edit', id=usuario.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}')

    return render_template('usuarios/edit.html', usuario=usuario)


@bp.route('/usuario/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado correctamente')
        return redirect(url_for('usuario.lista_usuarios'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el usuario: {str(e)}')
        return redirect(url_for('usuario.lista_usuarios'))

