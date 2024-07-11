# modulos/db.py
import mysql.connector

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="hotel"
)

cursor = conexion.cursor()

def verificar_credenciales(usuario, contraseña, tipo_usuario):
    if tipo_usuario == "encargado":
        cursor.execute("SELECT * FROM encargado WHERE correo = %s AND contraseña = %s", (usuario, contraseña))
    elif tipo_usuario == "administrador":
        cursor.execute("SELECT * FROM administrador WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
    
    result = cursor.fetchone()
    return result is not None
