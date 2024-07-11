from modulos.terminal import *
from modulos.db import cursor, conexion

# 5.- Registrar Reserva
def registrar_reserva():
    clear_console()
    print_box()
    solicitante = input("Ingrese el nombre del solicitante: ")
    fecha_reserva = input("Ingrese la fecha de la reserva (YYYY-MM-DD): ")
    fecha_checkout = input("Ingrese la fecha de checkout (YYYY-MM-DD): ")
    precio = int(input("Ingrese el precio de la reserva: "))
    fk_idEncargado = '0'

    # Insertar datos de la reserva en la base de datos
    sql_insert = "INSERT INTO reserva (solicitante, fecha_reserva, fecha_checkout, precio, fk_idEncargado) VALUES (%s, %s, %s, %s, %s)"
    val_insert = (solicitante, fecha_reserva, fecha_checkout, precio, fk_idEncargado)
    cursor.execute(sql_insert, val_insert)
    conexion.commit()

    print("\nReserva registrada correctamente.\nVolviendo al menú anterior")
    input("Presione Enter para continuar...")
