import os
import mysql.connector

##CONNECT
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="hotel"
)

class Habitaciones:
    def __init__(self, numero_habitacion, cantidad_pasajeros, orientacion, vacante):
        self.numero_habitacion = numero_habitacion
        self.cantidad_pasajeros = cantidad_pasajeros
        self.orientacion = orientacion
        self.vacante = vacante

    def mostrar_info(self):
        print(f"Tabla de Habitaciones")
        print(f"Número de Habitación: {self.numero_habitacion}, Cantidad de Pasajeros: {self.cantidad_pasajeros}, Orientación de la Habitación: {self.orientacion}, Vacante: {self.vacante}")


cursor = conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Habitaciones (idHabitacion INT AUTO_INCREMENT PRIMARY KEY, numero_habitacion INT UNIQUE, cantidad_pasajeros INT, orientacion VARCHAR(10), estado ENUM('ocupada', 'vacante'))")
cursor.execute("CREATE TABLE IF NOT EXISTS Asignaciones (id INT AUTO_INCREMENT PRIMARY KEY, numero_habitacion INT, nombre_responsable VARCHAR(255), rut_responsable VARCHAR(20), pasajero VARCHAR(255), fecha_asignacion DATE, hora_asignacion TIME)")

def verificar_credenciales(usuario, password):
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
    result = cursor.fetchone()
    return result is not None
