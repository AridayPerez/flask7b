from flask import Flask, render_template, request, redirect, flash, url_for
import pusher

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta'  # Necesaria para manejar 'flash' messages.

# Página principal con el formulario de registro
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para manejar el envío del formulario de registro
@app.route("/registro", methods=["POST"])
def registro():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")

    # Validación básica del formulario
    if len(username) < 5 or len(username) > 20 or not username.isalnum():
        flash("El nombre de usuario debe tener entre 5 y 20 caracteres y contener solo letras y números.")
        return redirect(url_for('index'))

    if len(password) < 8 or len(password) > 20:
        flash("La contraseña debe tener entre 8 y 20 caracteres.")
        return redirect(url_for('index'))

    if password != confirm_password:
        flash("Las contraseñas no coinciden.")
        return redirect(url_for('index'))

    # Si todo está correcto, se puede procesar el registro
    flash(f"Usuario {username} registrado con éxito.")
    return redirect(url_for('index'))

# Ruta para la página de alumnos
@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Ruta para guardar los datos de los alumnos
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Ruta para disparar un evento Pusher (si se necesita)
@app.route("/evento")
def evento():
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="cda1cc599395d699a2af",
        secret="9e9c00fc36600060d9e2",
        cluster="us2",
        ssl=True
    )
    pusher_client.trigger("my-channel", "my-event", {})
    return "Evento disparado."

if __name__ == "__main__":
    app.run(debug=True)
