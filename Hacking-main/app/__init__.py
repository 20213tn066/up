from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, Response, send_from_directory
import os
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail

# Inicialización de la aplicación Flask y sus extensiones
app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail()

# Configuración de la carpeta para subir archivos
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar el usuario en la sesión
@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db, id)

# Ruta para el inicio de sesión
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario(None, request.form['usuario'], request.form['password'], None, None, None, None, None, None, None)
        usuario_logueado = ModeloUsuario.login(db, usuario)
        if usuario_logueado != None:
            login_user(usuario_logueado)
            flash('Bienvenido', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

# Ruta para subir archivos
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No se ha enviado ningún archivo"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No se seleccionó ningún archivo"

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return f"El archivo {file.filename} ha sido subido. Ruta: {file_path}"

    return render_template('upload.html')

# Ruta para mostrar el formulario de subida de archivos
@app.route("/upload_form")
def upload_form():
    return render_template('upload.html')

# Ruta para servir archivos subidos
@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta de cierre de sesión
@app.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login'))

# Ruta principal del sitio
@app.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos = ModeloLibro.listar_libros_vendidos(db)
                data = {
                    'titulo': 'Libros vendidos',
                    'libros_vendidos': libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
        else:
            try:
                compras = ModeloCompra.listar_compras_usuario(db, current_user)
                data = {
                    'titulo': 'Mis compras',
                    'compras': compras
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
    else:
        return redirect(url_for('login'))

# Manejo de errores
def pagina_no_autorizada(error):
    return redirect(url_for('login'))

# Inicialización de la aplicación con configuración
def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    mail.init_app(app)
    app.register_error_handler(401, pagina_no_autorizada)
    return app
