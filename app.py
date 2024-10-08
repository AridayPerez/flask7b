# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import pusher

import mysql.connector
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()

    return render_template("app.html")

@app.route("/usuarios")
def usuarios():
    con.close()

    return render_template("usuarios.html")

@app.route("/usuarios/guardar", methods=["POST"])
def usuariosGuardar():
    con.close()
    nombre_usuario      = request.form["txtNombre_Usuario"]
    contrasena = request.form["txtContrasena"]

    return f"Nombre {nombre_usuario} Contrasena {contrasena}"

# Código usado en las prácticas
def notificarActualizacion():
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="2df86616075904231311",
        secret="2f91d936fd43d8e85a1a",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalRegistros", "registro", args)

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT id_Usuarios, Nombre_Usuario, Contrasena FROM tst0_usuarios
    ORDER BY id_Usuarios DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id_usuario          = request.form["id_Usuario"]
    nombre_usuario = request.form["Nombre_Usuario"]
    contrasena     = request.form["Contrasena"]
    
    cursor = con.cursor()

    if id_:
        sql = """
        UPDATE tst0_usuarios SET
        Nombre_Usuario = %s,
        Contrasena     = %s
        WHERE id_Usuario = %s
        """
        val = (nombre_usuario, contrasena, id_Usuario)
    else:
        sql = """
        INSERT INTO tst0_Usuarios (Nombre_Usuario, Contrasena)
                        VALUES (%s,          %s,      %s)
        """
        val =                  (Nombre_Usuario, Contrasena)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacion()

    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.args["id_Usuario"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT id_Usuario, Nombre_Usuario, Contrasena FROM tst0_Usuarios
    WHERE id_Usuario = %s
    """
    val    = (id_Usuario,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_Usuario"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM tst0_Usuarios
    WHERE id_Usuario = %s
    """
    val    = (id_Usuario,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacion()

    return make_response(jsonify({}))
