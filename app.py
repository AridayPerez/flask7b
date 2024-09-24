from flask import Flask, render_template, request, redirect, flash, url_for
import pusher

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta'

usuarios_registrados = []

@app.route("/")
def index():
    return render_template("app.html", usuarios=usuarios_registrados)

@app.route("/registro", methods=["POST"])
def registro():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")

    if len(username) < 5 or len(username) > 20 or not username.isalnum():
        flash("El nombre de usuario debe tener entre 5 y 20 caracteres y contener solo letras y números.")
        return redirect(url_for('index'))

    if len(password) < 8 or len(password) > 20:
        flash("La contraseña debe tener entre 8 y 20 caracteres.")
        return redirect(url_for('index'))

    if password != confirm_password:
        flash("Las contraseñas no coinciden.")
        return redirect(url_for('index'))

    pusher_client = pusher.Pusher(
        app_id='1766038',
        key='87d2c26ba36c6da2dc5f',
        secret='64785a24700ebcea228c',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    
    # Si todo está correcto, agregar usuario a la lista
    usuarios_registrados.append({'username': username, 'password': password})
    flash(f"Usuario {username} registrado con éxito.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
