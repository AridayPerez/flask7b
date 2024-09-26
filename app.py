from flask import Flask, render_template, request
import mysql.connector
import bcrypt

app = Flask(__name__)

# Configuración de la base de datos (ajusta los valores)
mydb = mysql.connector.connect(
  host="tu_host",
  user="tu_usuario",
  password="tu_contraseña",
  database="tu_base_de_datos"
)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insertar los datos en la base de datos
    mycursor = mydb.cursor()
    sql = "INSERT INTO tst0_usuarios (username, email, password) VALUES (%s, %s, %s)"
    val = (username, email, hashed_password)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        return "Usuario registrado exitosamente"
    except mysql.connector.Error as error:
        return f"Error al registrar el usuario: {error}"

if __name__ == "__main__":
    app.run(debug=True)
