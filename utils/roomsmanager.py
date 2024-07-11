from utils.database import cursor, conexion
from utils.terminal import *
from prettytable import PrettyTable

def ag_habitacion():
    numero_habitacion = int(input("Ingrese el número de habitación: "))
    cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))
    orientaciones = ["Norte", "Sur", "Este", "Oeste"]
    orientacion = select_option(orientaciones)
    print("Selecciona la orientación de la habitación")
    ocupada = '0'

    sql = "INSERT INTO Habitaciones (numero_habitacion, cantidad_pasajeros, orientacion, ocupada) VALUES (%s, %s, %s, %s)"
    val = (numero_habitacion, cantidad_pasajeros, orientacion, ocupada)
    cursor.execute(sql, val)
    conexion.commit()
    print("Habitacion agregada correctamente.")

def ver_lista_habitaciones():
    clear_console()
    print_box()
    cursor.execute("SELECT * FROM Habitaciones")
    habitaciones = cursor.fetchall()

    if not habitaciones:
        print("No hay habitaciones registradas.")
        return

    tabla = PrettyTable()
    tabla.field_names = ["ID", "Número de Habitación", "Cantidad de Pasajeros", "Orientación", "Ocupada", "fk_reserva"]

    for habitacion in habitaciones:
        tabla.add_row(habitacion)

    print(tabla)
    input("Presione Enter para continuar...")

def registrar_reserva():
    clear_console()
    print_box()
    solicitante = input("Ingrese el nombre del solicitante: ")
    fecha_reserva = input("Ingrese la fecha de la reserva (YYYY-MM-DD): ")
    fecha_checkout = input("Ingrese la fecha de checkout (YYYY-MM-DD): ")
    precio = int(input("Ingrese el precio de la reserva: "))
    fk_idEncargado = '0'

    sql_insert = "INSERT INTO reserva (solicitante, fecha_reserva, fecha_checkout, precio, fk_idEncargado) VALUES (%s, %s, %s, %s, %s)"
    val_insert = (solicitante, fecha_reserva, fecha_checkout, precio, fk_idEncargado)
    cursor.execute(sql_insert)
    conexion.commit()

    print("\nReserva registrada correctamente.\nVolviendo al menú anterior")
    input("Presione Enter para continuar...")
