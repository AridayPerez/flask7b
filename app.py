from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/usuarios/buscar")
def buscar_usuarios():
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT Id_Usuario, NombreUsuario, Contrasena FROM tst0_usuarios
        ORDER BY Id_Usuario DESC
    """)
    registros = cursor.fetchall()
    con.close()
    return make_response(jsonify(registros))

@app.route("/usuarios/guardar", methods=["POST"])
def guardar_usuario():
    con = get_connection()
    id_usuario = request.form.get("Id_Usuario")
    nombre_usuario = request.form["NombreUsuario"]
    contrasena = request.form["Contrasena"]

    cursor = con.cursor()

    if id_usuario:
        # Actualización de usuario existente
        sql = """
            UPDATE tst0_usuarios SET
            NombreUsuario = %s,
            Contrasena = %s
            WHERE Id_Usuario = %s
        """
        val = (nombre_usuario, contrasena, id_usuario)
    else:
        # Inserción de nuevo usuario
        sql = """
            INSERT INTO tst0_usuarios (NombreUsuario, Contrasena)
            VALUES (%s, %s)
        """
        val = (nombre_usuario, contrasena)

    cursor.execute(sql, val)
    con.commit()  # Asegurarse de que los cambios se guarden
    con.close()

    return make_response(jsonify({"status": "success"}))

@app.route("/usuarios/editar", methods=["GET"])
def editar_usuario():
    con = get_connection()
    id_usuario = request.args["Id_Usuario"]
    cursor = con.cursor(dictionary=True)
    sql = """
        SELECT Id_Usuario, NombreUsuario, Contrasena FROM tst0_usuarios
        WHERE Id_Usuario = %s
    """
    val = (id_usuario,)

    cursor.execute(sql, val)
    registro = cursor.fetchone()
    con.close()

    return make_response(jsonify(registro))

@app.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuario():
    con = get_connection()
    id_usuario = request.form["Id_Usuario"]

    cursor = con.cursor()
    sql = """
        DELETE FROM tst0_usuarios
        WHERE Id_Usuario = %s
    """
    val = (id_usuario,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"status": "success"}))

if __name__ == "__main__":
    app.run(debug=True)
