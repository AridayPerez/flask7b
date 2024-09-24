from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta'

# Lista en memoria para almacenar los usuarios registrados
usuarios_registrados = []

# Página principal con el formulario de registro y tabla de usuarios
@app.route("/")
def index():
    return render_template("app.html", usuarios=usuarios_registrados)

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

    # Si todo está correcto, agregar usuario a la lista
    usuarios_registrados.append({'username': username, 'password': password})
    flash(f"Usuario {username} registrado con éxito.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
