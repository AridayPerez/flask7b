from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify, make_response

import pusher
import mysql.connector

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

def check_connection():
    if not con.is_connected():
        con.reconnect()

@app.route("/")
def index():
    con.close()
    return render_template("app.html")

def notificarActualizacion():
    pusher_client = pusher.Pusher(
    app_id='1766038',
    key='87d2c26ba36c6da2dc5f',
    secret='64785a24700ebcea228c',
    cluster='us2',
    ssl=True
    )

    args = {}  # Puedes definir los datos que deseas enviar
    pusher_client.trigger("canalRegistrosusuarioss", "registrousuarioss", args)

@app.route("/buscar")
def buscar():
    check_connection()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios
    ORDER BY Id_Usuario DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()
    return make_response(jsonify(registros))

# Ruta para guardar registros (insertar o actualizar)
@app.route("/guardar", methods=["POST"])
def guardar():
    check_connection()

    id = request.form["id"]
    nombre = request.form["nombre"]
    contrasena = request.form["contrasena"]
    cursor = con.cursor()

    if id:  # Si se proporciona el ID, es una actualización
        sql = """
        UPDATE tst0_usuarios SET
        Nombre_Usuario = %s,
        Contrasena     = %s,
        WHERE Id_Usuario = %s
        """
        val = (nombre, contrasena, id)
    else:  # Si no hay ID, es una inserción
        sql = """
        INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena)
        VALUES (%s, %s, %s)
        """
        val = (nombre, contrasena)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacion()

    return make_response(jsonify({}))

# Ruta para editar un registro (obtener datos de un registro específico)
@app.route("/editar", methods=["GET"])
def editar():
    check_connection()

    id = request.args["id"]
    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()

    con.close()
    return make_response(jsonify(registros))

# Ruta para eliminar un registro
@app.route("/eliminar", methods=["POST"])
def eliminar():
    check_connection()

    id = request.form["id"]
    cursor = con.cursor(dictionary=True)
    sql = """
    DELETE FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacion()

    return make_response(jsonify({}))
