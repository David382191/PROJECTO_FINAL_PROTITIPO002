from flask import Blueprint, render_template
import mysql.connector

secretaria_bp = Blueprint("secretaria", __name__)

# Conexión a BD
conexion = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="12345",
    database="chatbot_secretaria"
)

@secretaria_bp.route("/registro/secretaria")
def mostrar_secretarias():
    cursor = conexion.cursor(dictionary=True)

    # Consulta SOLO la tabla admin_secretaria
    cursor.execute("""
        SELECT CEDULA, Nombre, Apellido, Usuario, Contrasena_hash, Telefono 
        FROM admin_secretaria
    """)

    datos = cursor.fetchall()

    return render_template("registro-admin.html", registros=datos)
