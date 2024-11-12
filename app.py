from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import pusher
import logging
from flask_cors import CORS

# Configuración del logger de Flask
logging.basicConfig(level=logging.INFO)

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

app = Flask(__name__)
CORS(app)

# Inicialización de Pusher
pusher_client = pusher.Pusher(
    app_id="1766038",
    key="87d2c26ba36c6da2dc5f",
    secret="64785a24700ebcea228c",
    cluster="us2",
    ssl=True
)

# Página principal
@app.route("/")
def index():
    logging.info("Cargando la página principal.")
    return render_template("app.html")

# Crear o actualizar un usuario
@app.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    # Validar que los campos no estén vacíos
    nombre_usuario = request.form.get("nombre_usuario")
    contrasena = request.form.get("contrasena")

    if not nombre_usuario or not contrasena:
        logging.warning("Faltan datos obligatorios: 'nombre_usuario' o 'contrasena'.")
        return make_response(jsonify({"error": "Los campos 'nombre_usuario' y 'contrasena' son obligatorios."}), 400)

    con = get_db_connection()
    id_usuario = request.form.get("id_usuario")

    cursor = con.cursor()
    if id_usuario:  # Actualizar usuario existente
        sql = """
        UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s
        """
        val = (nombre_usuario, contrasena, id_usuario)
        logging.info(f"Actualizando usuario con ID: {id_usuario}")
    else:  # Crear un nuevo usuario
        sql = """
        INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)
        """
        val = (nombre_usuario, contrasena)
        logging.info(f"Creando nuevo usuario: {nombre_usuario}")

    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_usuarios()
    return make_response(jsonify({"message": "Usuario guardado exitosamente"}))

# Obtener todos los usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    con.close()

    logging.info("Obteniendo la lista de todos los usuarios.")
    return make_response(jsonify(usuarios))

# Obtener un usuario por ID sin usar query string
@app.route("/usuarios/editar/<int:id_usuario>", methods=["GET"])
def editar_usuario(id_usuario):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM tst0_usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()
    cursor.close()
    con.close()

    logging.info(f"Obteniendo datos del usuario con ID: {id_usuario}")
    return make_response(jsonify(usuario))

# Eliminar un usuario usando el ID en la URL
@app.route("/usuarios/eliminar/<int:id_usuario>", methods=["POST"])
def eliminar_usuario(id_usuario):
    logging.info(f"Intentando eliminar el usuario con ID: {id_usuario}")

    con = get_db_connection()
    cursor = con.cursor()
    sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)
    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_usuarios()
    logging.info(f"Usuario con ID {id_usuario} eliminado exitosamente.")
    return make_response(jsonify({"message": "Usuario eliminado exitosamente"}))

# Notificación de actualizaciones usando Pusher
def notificar_actualizacion_usuarios():
    pusher_client.trigger("canalUsuarios", "actualizacion", {})
    logging.info("Notificación de actualización enviada a través de Pusher")

if __name__ == "__main__":
    app.run(debug=True)
