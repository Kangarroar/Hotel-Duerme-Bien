import mysql.connector

# CONNECT
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="hotel"
)

cursor = conexion.cursor()

def verificar_credenciales(encargado, contraseña):
    cursor.execute("SELECT * FROM encargado WHERE correo = %s AND contraseña = %s", (encargado, contraseña))
    result = cursor.fetchone()
    return result is not None
