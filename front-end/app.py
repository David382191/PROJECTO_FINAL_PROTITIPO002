## Alfonso Espinoza.

##Aquí primero vamos a traer las librerías que usaremos aquí.
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from controllers.home_routes import home_bp

from controllers.registro_secretaria_routers import secretaria_bp



# CREAR APP DE FLASK
app = Flask(__name__)

# CLAVE PARA USAR SESSION
app.secret_key = "clave_super_secreta_123"

# Registrar las rutas del blueprint
app.register_blueprint(home_bp)
app.register_blueprint(secretaria_bp)

# Conexión a la BD
conexion = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="12345",
    database="chatbot_secretaria"
)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        password = request.form["password"]

        #Aquí vamos a necesitar usar consultas SQL, por lo que
        # necesitamremos abrir un lugar donde ejecutarlas,
        # eso lo que hace esto de aquí abajo. 
        cursor = conexion.cursor(dictionary=True)

        #de esta forma podemos hacer consultas a la base de datos SQL como esta.
        #Los %s evitan SQL Injection. Mientras que se leeran los valores que enviamos.
        cursor.execute("SELECT * FROM admin_secretaria a WHERE Usuario=%s AND Contrasena_Hash=%s",
                       (usuario, password))
        
        admin = cursor.fetchone()

        ##Aquí es donde funciona el redirecionamiento.
        if admin:
            session["admin_id"] = admin["CEDULA"]
            ##Si todo está bien, nos enviará a este lugar. Aquí es donde podemos cambiarlo.
            return redirect("/home")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


@app.route("/home")
def panel():
    if "admin_id" not in session:
        return redirect("/")
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)