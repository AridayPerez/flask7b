from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
import bcrypt
import mysql.connector
from mysql.connector import Error
import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta'  # Cambia esto por una clave secreta segura

def get_db_connection():
    """
    Función para establecer una conexión con la base de datos.
    """
    try:
        connection = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst0_usuarios",
            password="dJ0CIAFF="
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route("/")
def index():
    """
    Ruta principal que muestra el formulario de registro y la tabla de usuarios.
    """
    connection = get_db_connection()
    usuarios = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT Id_Usuario, Nombre_Usuario FROM tst0_usuarios ORDER BY Id_Usuario DESC")
            usuarios = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
        finally:
            cursor.close()
            connection.close()
    return render_template("app.html", usuarios=usuarios)

@app.route("/registrar", methods=["POST"])
def registrar():
    """
    Ruta para manejar el registro de nuevos usuarios.
    """
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")

    # Validaciones del lado del servidor
    if not username or not password or not confirm_password:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('index'))

    if len(username) < 5 or len(username) > 20:
        flash("El nombre de usuario debe tener entre 5 y 20 caracteres.", "danger")
        return redirect(url_for('index'))

    if not username.isalnum():
        flash("El nombre de usuario solo puede contener letras y números.", "danger")
        return redirect(url_for('index'))

    if len(password) < 8 or len(password) > 20:
        flash("La contraseña debe tener entre 8 y 20 caracteres.", "danger")
        return redirect(url_for('index'))

    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "danger")
        return redirect(url_for('index'))

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insertar los datos en la base de datos
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
        val = (username, hashed_password.decode('utf-8'))
        try:
            cursor.execute(sql, val)
            connection.commit()
            flash(f"Usuario '{username}' registrado exitosamente.", "success")
        except Error as e:
            flash(f"Error al registrar el usuario: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
    else:
        flash("No se pudo conectar a la base de datos.", "danger")

    return redirect(url_for('index'))

@app.route("/buscar")
def buscar():
    """
    Ruta para obtener los usuarios registrados en formato JSON.
    """
    connection = get_db_connection()
    usuarios = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT Id_Usuario, Nombre_Usuario FROM tst0_usuarios ORDER BY Id_Usuario DESC")
            usuarios = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
        finally:
            cursor.close()
            connection.close()
    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(debug=True)
