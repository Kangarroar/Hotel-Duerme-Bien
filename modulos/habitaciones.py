from modulos.terminal import *
from prettytable import PrettyTable
from modulos.db import cursor, conexion

# 1.- Agregar habitacion
def ag_habitacion():
    numero_habitacion = int(input("Ingrese el número de habitación: "))
    cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))
    orientaciones = ["Norte", "Sur", "Este", "Oeste"]
    orientacion = select_option(orientaciones) 
    print("Selecciona la orientación de la habitación")
    ocupada = '0'  # Nuevo estado por defecto para una nueva habitación

    sql = "INSERT INTO Habitaciones (numero_habitacion, cantidad_pasajeros, orientacion, ocupada) VALUES (%s, %s, %s, %s)"
    val = (numero_habitacion, cantidad_pasajeros, orientacion, ocupada)
    cursor.execute(sql, val)
    conexion.commit()
    print("Habitacion agregada correctamente.")

#3.- Mostrar habitaciones
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
