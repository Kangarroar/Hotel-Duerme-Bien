from modulos.terminal import clear_console, print_box, select_option
from prettytable import PrettyTable
from modulos.db import cursor, conexion
from datetime import datetime

# 2.- Registrar Pasajeros
def registrar_pasajeros():
    cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))

    ruts_pasajeros = []
    nombres_pasajeros = []
    for i in range(cantidad_pasajeros):
        rut = input(f"Ingrese el RUT del pasajero {i + 1}: ")
        nombre = input(f"Ingrese el nombre del pasajero {i + 1}: ")
        ruts_pasajeros.append(rut)
        nombres_pasajeros.append(nombre)

    print("\nLista de pasajeros registrados:")
    for rut, nombre in zip(ruts_pasajeros, nombres_pasajeros):
        print(f"RUT: {rut}, Nombre: {nombre}")

    # Selector de pasajero responsable con flechitas
    print("\nSeleccione el pasajero responsable:")
    selected_index = select_option(nombres_pasajeros, return_index=True)
    nombre_responsable = nombres_pasajeros[selected_index]
    rut_responsable = ruts_pasajeros[selected_index]

    # Verificar la existencia y estado de la habitación
    numero_habitacion = input("Ingrese el número de la habitación a asignar: ")
    cursor.execute("SELECT estado FROM Habitaciones WHERE numero_habitacion = %s", (numero_habitacion,))
    habitacion_info = cursor.fetchone()

    if habitacion_info is None:
        print("La habitación no existe.")
        return
    elif habitacion_info[0] != "vacante":
        print("La habitación no está disponible para ser asignada.")
        return

    fecha_asignacion = datetime.now().date()
    hora_asignacion = datetime.now().time()

    # Insertar datos en la base de datos para cada pasajero
    for rut, nombre in zip(ruts_pasajeros, nombres_pasajeros):
        sql_insert = "INSERT INTO Asignaciones (numero_habitacion, nombre_responsable, rut_responsable, pasajero, fecha_asignacion, hora_asignacion) VALUES (%s, %s, %s, %s, %s, %s)"
        val_insert = (numero_habitacion, nombre_responsable, rut_responsable, nombre, fecha_asignacion, hora_asignacion)
        cursor.execute(sql_insert, val_insert)

    # Cambiar el estado de la habitación a "ocupada"
    cursor.execute("UPDATE Habitaciones SET estado = 'ocupada' WHERE numero_habitacion = %s", (numero_habitacion,))
    conexion.commit()

    print("\nRegistro de pasajeros realizado correctamente.\nVolviendo al menú anterior")
    input("Presione Enter para continuar...")

#4.- Ver lista de pasajeros
def ver_tabla_resumen():
    clear_console()
    print_box()
    # Consulta a la base de datos para obtener los pasajeros hospedados
    cursor.execute("SELECT numero_habitacion, pasajero, fecha_asignacion, hora_asignacion FROM Asignaciones")
    asignaciones = cursor.fetchall()

    # Crear la tabla resumen con PrettyTable
    tabla_resumen = PrettyTable()
    tabla_resumen.field_names = ["Habitación", "Nombre del Pasajero", "Fecha de Check-In", "Hora de Check-In"]

    for asignacion in asignaciones:
        numero_habitacion, pasajero, fecha_asignacion, hora_asignacion = asignacion
        tabla_resumen.add_row([numero_habitacion, pasajero, fecha_asignacion, hora_asignacion])

    # Mostrar la tabla resumen
    print("\nTabla Resumen de Pasajeros Hospedados")
    print(tabla_resumen)
    input("Presione Enter para continuar...")
