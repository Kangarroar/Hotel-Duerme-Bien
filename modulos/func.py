import msvcrt
import os
from modulos.db import *
from datetime import datetime
import time
from prettytable import PrettyTable


# limpiador
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# UI Prints
def print_options(options, selected_index):
    clear_console()
    print_box()
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"\033[92m> {option}\033[0m")
        else:
            print(option)

# Print box
def print_box():
    print("┌───────────────────────────────┐")
    print("│ Sistema de pasajeros de hotel │")
    print("└───────────────────────────────┘\n")


# Selector with arrow keys
def select_option(options, return_index=False):
    selected_index = 0
    print_options(options, selected_index)

    while True:
        key = ord(msvcrt.getch())

        if key == 72:  # Up arrow key
            selected_index = (selected_index - 1) % len(options)
        elif key == 80:  # Down arrow key
            selected_index = (selected_index + 1) % len(options)
        elif key == 13:  # Enter key
            if return_index:
                return selected_index  # Devolver el índice seleccionado
            else:
                return options[selected_index]  # Devolver el elemento seleccionado

        print_options(options, selected_index)


# Manage rooms submenu
def manage_rooms():
    add_option = '1.- Agregar habitacion'
    delete_option = '2.- Eliminar habitacion'
    back_option = '3.- Volver atras'
    options = [add_option, delete_option, back_option]

    while True:
        selected_option = select_option(options)

        if selected_option == add_option:
            print("Opción para agregar habitación seleccionada.")
            clear_console()
            ag_habitacion()
            input("Presione Enter para continuar...")
        elif selected_option == delete_option:
            print("Opción para eliminar habitación seleccionada.")
            input("Presione Enter para continuar...")
        elif selected_option == back_option:
            return

# Template for "Registrar pasajeros"
def register_passengers():
    print("Opción para registrar pasajeros seleccionada.")
    input("Presione Enter para continuar...")

# Template for "Ver lista de habitaciones"
def view_rooms_list():
    print("Opción para ver lista de habitaciones seleccionada.")
    input("Presione Enter para continuar...")


# Main menu
def main_menu():
    manage_rooms_option = '1.- Administrar habitaciones'
    register_option = '2.- Registrar pasajeros'
    view_rooms_option = '3.- Ver lista de habitaciones'
    view_pasajeros_option = '4.- Ver lista de pasajeros'
    exit_option = 'Salir'
    options = [manage_rooms_option, register_option, view_rooms_option, view_pasajeros_option, exit_option]

    while True:
        selected_option = select_option(options)
        
        if selected_option == manage_rooms_option:
            manage_rooms()
        elif selected_option == register_option:
            registrar_pasajeros()
        elif selected_option == view_rooms_option:
            ver_lista_habitaciones()
        elif selected_option == view_pasajeros_option:
            ver_tabla_resumen()
        elif selected_option == exit_option:
            break

def login():
    max_intentos = 3
    intentos = 0
    
    while intentos < max_intentos:
        print_box()
        print("Iniciar sesión\n")
        usuario = input("Usuario: ")
        password = input("Contraseña: ")

        # Verificar el usuario y la contraseña en la base de datos
        if verificar_credenciales(usuario, password):
            print("Inicio de sesión exitoso.")
            return True
        else:
            intentos += 1
            print(f"Usuario o contraseña incorrectos. Intento {intentos} de {max_intentos}")
    
    print("Has excedido el número máximo de intentos. Vuelve a iniciar el programa.")
    return False

#####
# 1.- Agregar habitacion
def ag_habitacion():
    numero_habitacion = int(input("Ingrese el número de habitación: "))
    cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))
    orientaciones = ["Norte", "Sur", "Este", "Oeste"]
    orientacion = select_option(orientaciones) 
    print("Selecciona la orientación de la habitación")
    estado = 'vacante'  # Nuevo estado por defecto para una nueva habitación

    sql = "INSERT INTO Habitaciones (numero_habitacion, cantidad_pasajeros, orientacion, estado) VALUES (%s, %s, %s, %s)"
    val = (numero_habitacion, cantidad_pasajeros, orientacion, estado)
    cursor.execute(sql, val)
    conexion.commit()
    print("Habitacion agregada correctamente.")

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
    tabla.field_names = ["ID", "Número de Habitación", "Cantidad de Pasajeros", "Orientación", "Estado"]

    for habitacion in habitaciones:
        tabla.add_row(habitacion)

    print(tabla)
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

    