from utils.database import cursor, conexion
from utils.terminal import *
from prettytable import PrettyTable
from datetime import datetime

def ver_tabla_resumen():
    clear_console()
    print_box()
    cursor.execute("SELECT numero_habitacion, pasajero, fecha_asignacion, hora_asignacion FROM Asignaciones")
    asignaciones = cursor.fetchall()

    tabla_resumen = PrettyTable()
    tabla_resumen.field_names = ["Habitación", "Nombre del Pasajero", "Fecha de Check-In", "Hora de Check-In"]

    for asignacion in asignaciones:
        numero_habitacion, pasajero, fecha_asignacion, hora_asignacion = asignacion
        tabla_resumen.add_row([numero_habitacion, pasajero, fecha_asignacion, hora_asignacion])

    print("\nTabla Resumen de Pasajeros Hospedados")
    print(tabla_resumen)
    input("Presione Enter para continuar...")
