import msvcrt
import os
from prettytable import PrettyTable
from utils.database import cursor, conexion
from datetime import datetime

############### UI ###############

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

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


# Selector
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
                return selected_index
            else:
                return options[selected_index]

        print_options(options, selected_index)


############### UI Menu Principal ###############

def main_menu():
    manage_rooms_option = '1.- Administrar habitaciones'
    register_option = '2.- Registrar pasajeros'
    view_rooms_option = '3.- Ver lista de habitaciones'
    view_pasajeros_option = '4.- Ver lista de pasajeros'
    register_reserva_option = '5.- Registrar reserva'
    exit_option = 'Salir'
    options = [manage_rooms_option, register_option, view_rooms_option, view_pasajeros_option, register_reserva_option, exit_option]

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
        elif selected_option == register_reserva_option:
            registrar_reserva()
        elif selected_option == exit_option:
            break

############### Submenu de Administrar habitaciones ###############
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
        elif selected_option == delete_option:
            print("Opción para eliminar habitación seleccionada.")
            clear_console()
            eliminar_habitacion()
        elif selected_option == back_option:
            return
        
############### Agregar Habitacion ###############

def ag_habitacion():
    try:
        numero_habitacion = int(input("Ingrese el número de habitación: "))
        cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))
    except ValueError:
        print("Error: Debes ingresar un número entero para el número de habitación y la cantidad de pasajeros.")
        return

    orientaciones = ["Norte", "Sur", "Este", "Oeste"]
    orientacion = select_option(orientaciones)
    print("Selecciona la orientación de la habitación")
    ocupada = '0'

    try:
        sql = "INSERT INTO Habitaciones (numero_habitacion, cantidad_pasajeros, orientacion, ocupada) VALUES (%s, %s, %s, %s)"
        val = (numero_habitacion, cantidad_pasajeros, orientacion, ocupada)
        cursor.execute(sql, val)
        conexion.commit()
        print("Habitacion agregada correctamente.")
        input("Presione Enter para continuar...")
    except Exception as e:
        print(f"Error al agregar la habitación: {e}")
        input("Presione Enter para continuar...")


############### Ver Lista Habitaciones ###############

def ver_lista_habitaciones():
    clear_console()
    print_box()
    cursor.execute("SELECT numero_habitacion, cantidad_pasajeros, orientacion, ocupada FROM Habitaciones")
    habitaciones = cursor.fetchall()

    if not habitaciones:
        print("No hay habitaciones registradas.")
        return

    tabla = PrettyTable()
    tabla.field_names = ["Número de Habitación", "Cantidad de Pasajeros", "Orientación", "Ocupada"]

    for habitacion in habitaciones:
        numero_habitacion, cantidad_pasajeros, orientacion, ocupada = habitacion
        if ocupada == 0:
            ocupada_texto = "No"
        elif ocupada == 1:
            ocupada_texto = "Sí"
        else:
            ocupada_texto = "Desconocido" #catch

        tabla.add_row([numero_habitacion, cantidad_pasajeros, orientacion, ocupada_texto])

    print(tabla)
    input("Presione Enter para continuar...")



############### Eliminar Habitacion ###############

def eliminar_habitacion():
    ver_lista_habitaciones()

    try:
        numero_habitacion = int(input("Ingrese el número de habitación a eliminar: "))
    except ValueError:
        print("Error: Debes ingresar un número entero para el número de habitación.")
        return

    cursor.execute("SELECT ocupada FROM Habitaciones WHERE numero_habitacion = %s", (numero_habitacion,))
    result = cursor.fetchone()

    if not result:
        print("Error: La habitación no existe.")
        return

    ocupada = result[0]
    if ocupada == '1':
        print("Error: La habitación está ocupada y no puede ser eliminada.")
        return

    try:
        cursor.execute("DELETE FROM Habitaciones WHERE numero_habitacion = %s", (numero_habitacion,))
        conexion.commit()
        print("Habitación eliminada correctamente.")
        input("Presione Enter para continuar...")
    except Exception as e:
        print(f"Error al eliminar la habitación: {e}")
        input("Presione Enter para continuar...")


############### Registrar Reserva ###############
def registrar_reserva():
    clear_console()
    print_box()
    
    solicitante = input("Ingrese el nombre del solicitante: ")

    while True:
        fecha_reserva = input("Ingrese la fecha de la reserva (YYYY-MM-DD): ")
        try:
            fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Error: Fecha no válida. Por favor, ingrese una fecha en el formato YYYY-MM-DD.")
    
    while True:
        fecha_checkout = input("Ingrese la fecha de checkout (YYYY-MM-DD): ")
        try:
            fecha_checkout = datetime.strptime(fecha_checkout, '%Y-%m-%d').date()
            if fecha_checkout > fecha_reserva:
                break
            else:
                print("Error: La fecha de checkout debe ser posterior a la fecha de reserva.")
        except ValueError:
            print("Error: Fecha no válida. Por favor, ingrese una fecha en el formato YYYY-MM-DD.")
    
    while True:
        try:
            cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))
            break
        except ValueError:
            print("Error: Debes ingresar un número entero para la cantidad de pasajeros.")
    
    while True:
        try:
            ver_lista_habitaciones()
            habitacion_reservada = int(input("Ingrese el número de la habitación reservada: "))
            break
        except ValueError:
            print("Error: Debes ingresar un número entero para el número de habitación.")
    
    fk_idEncargado = '0'
    
    # Calcular costo
    costo_por_pasajero = 20000
    costo_total = cantidad_pasajeros * costo_por_pasajero

    sql_insert = "INSERT INTO reserva (solicitante, fecha_reserva, fecha_checkout, precio, pasajeros, habitacion_reservada, fk_idEncargado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val_insert = (solicitante, fecha_reserva, fecha_checkout, costo_total, cantidad_pasajeros, habitacion_reservada, fk_idEncargado)
    
    try:
        # Validar disponibilidad
        cursor.execute("SELECT fecha_reserva, fecha_checkout FROM reserva WHERE habitacion_reservada = %s", (habitacion_reservada,))
        reservas_exist = cursor.fetchall()

        for reserva in reservas_exist:
            reserva_fecha_reserva, reserva_fecha_checkout = reserva
            if not (fecha_checkout < reserva_fecha_reserva or fecha_reserva > reserva_fecha_checkout):
                print(f"La habitación {habitacion_reservada} no está disponible para las fechas solicitadas.")
                return
        
        cursor.execute(sql_insert, val_insert)
        conexion.commit()
        print("\nReserva registrada correctamente.\nVolviendo al menú anterior")
    except Exception as e:
        print(f"Error al registrar la reserva: {e}")

    input("Presione Enter para continuar...")


############### Registrar Pasajeros ###############

def registrar_pasajeros():
    clear_console()
    print_box()
    try:
        cantidad_pasajeros = int(input("Ingrese la cantidad de pasajeros: "))
    except ValueError:
        print("Error: Debes ingresar un número entero para la cantidad de pasajeros.")
        input("Presione Enter para continuar...")
        return

    ruts_pasajeros = []
    nombres_pasajeros = []
    for i in range(cantidad_pasajeros):
        while True:
            rut = input(f"Ingrese el RUT del pasajero {i + 1}: ")
            if rut.isdigit():
                break
            else:
                print("Error: El RUT solo puede contener números. Inténtalo de nuevo.")
                input("Presione Enter para continuar...")
        nombre = input(f"Ingrese el nombre del pasajero {i + 1}: ")
        ruts_pasajeros.append(rut)
        nombres_pasajeros.append(nombre)

    print("\nLista de pasajeros registrados:")
    for rut, nombre in zip(ruts_pasajeros, nombres_pasajeros):
        print(f"RUT: {rut}, Nombre: {nombre}")

    print("\nSeleccione el pasajero responsable:")
    selected_index = select_option(nombres_pasajeros, return_index=True)
    nombre_responsable = nombres_pasajeros[selected_index]
    rut_responsable = ruts_pasajeros[selected_index]
    
    ver_lista_habitaciones()
    numero_habitacion = input("Ingrese el número de la habitación a asignar: ")
    cursor.execute("SELECT ocupada FROM Habitaciones WHERE numero_habitacion = %s", (numero_habitacion,))
    habitacion_info = cursor.fetchone()

    if habitacion_info is None:
        print("La habitación no existe.")
        return
    elif habitacion_info[0] == '1':  # Assuming '1' means occupied and '0' means not occupied
        print("La habitación no está disponible para ser asignada.")
        return

    print("\nSeleccione la reserva por:")
    cursor.execute("SELECT solicitante FROM reserva")
    reservas = cursor.fetchall()
    solicitantes = [reserva[0] for reserva in reservas]

    if not solicitantes:
        print("No hay reservas disponibles.")
        return

    solicitante_index = select_option(solicitantes, return_index=True)
    reservado_por = solicitantes[solicitante_index]

    fecha_asignacion = datetime.now().date()
    hora_asignacion = datetime.now().time()

    for rut, nombre in zip(ruts_pasajeros, nombres_pasajeros):
        sql_insert = "INSERT INTO Asignaciones (numero_habitacion, nombre_responsable, rut_responsable, pasajero, fecha_asignacion, hora_asignacion, reservado_por) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val_insert = (numero_habitacion, nombre_responsable, rut_responsable, nombre, fecha_asignacion, hora_asignacion, reservado_por)
        cursor.execute(sql_insert, val_insert)

    cursor.execute("UPDATE Habitaciones SET ocupada = '1' WHERE numero_habitacion = %s", (numero_habitacion,))
    conexion.commit()

    print("\nRegistro de pasajeros realizado correctamente.\nVolviendo al menú anterior")
    input("Presione Enter para continuar...")

############### Ver Tabla Resumen ###############

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

############### Admin Menu ###############

def admin_menu():
    add_encargado_option = '1.- Agregar encargado'
    delete_encargado_option = '2.- Eliminar encargado'
    back_option = 'Cerrar sesión'
    options = [add_encargado_option, delete_encargado_option, back_option]

    while True:
        selected_option = select_option(options)

        if selected_option == add_encargado_option:
            print("Opción para agregar encargado seleccionada.")
            agregar_encargado()
        elif selected_option == delete_encargado_option:
            print("Opción para eliminar encargado seleccionada.")
            eliminar_encargado()
        elif selected_option == back_option:
            return

############### Agregar Encargado ###############

def agregar_encargado():
    clear_console()
    print_box()

    try:
        nombre = input("Ingrese el nombre del encargado: ")
        edad = int(input("Ingrese la edad del encargado: "))
        if edad < 0: #uno nunca sabe
            print("Error: La edad debe ser un número positivo.")
            input("Presione Enter para continuar...")
            return
        
        fecha_nacimiento = input("Ingrese la fecha de nacimiento del encargado (YYYY-MM-DD): ")
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        except ValueError:
            print("Error: Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
            input("Presione Enter para continuar...")
            return
        
        correo = input("Ingrese el correo del encargado: ")

        telefono = input("Ingrese el teléfono del encargado: ")
    
        contraseña = input("Ingrese la contraseña del encargado: ")

        rut = input("Ingrese el rut del encargado: ")
        
        sql_insert = "INSERT INTO encargado (nombre, edad, fecha_nacimiento, correo, telefono, contraseña, rut) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val_insert = (nombre, edad, fecha_nacimiento, correo, telefono, contraseña, rut)
        
        cursor.execute(sql_insert, val_insert)
        conexion.commit()

        print("\nEncargado agregado correctamente.")

    except ValueError:
        print("Error: Ingresa un valor válido para la edad.")
    except Exception as e:
        print(f"Error al agregar encargado: {e}")

    input("\nPresione Enter para continuar...")

############### Eliminar Encargado ###############

def eliminar_encargado():
    clear_console()
    print_box()
    
    try:
        # Mostrar la tabla de encargados con sus IDs y nombres
        cursor.execute("SELECT idEncargado, nombre FROM encargado")
        encargados = cursor.fetchall()
        
        if not encargados:
            print("No hay encargados registrados.")
            input("Presione Enter para continuar...")
            return
        
        tabla_encargados = PrettyTable()
        tabla_encargados.field_names = ["ID Encargado", "Nombre"]
        
        for encargado in encargados:
            tabla_encargados.add_row([encargado[0], encargado[1]])
        
        print("Lista de encargados:")
        print(tabla_encargados)
        
        id_encargado = int(input("Ingrese el ID del encargado a eliminar: "))
        
        #mas validadores siiiiiiiiii
        if id_encargado not in [encargado[0] for encargado in encargados]:
            print("El ID del encargado no existe.")
            input("Presione Enter para continuar...")
            return
        
        sql_delete = "DELETE FROM encargado WHERE idEncargado = %s"
        val_delete = (id_encargado,)
        
        cursor.execute(sql_delete, val_delete)
        conexion.commit()
        
        print("\nEncargado eliminado correctamente.")
        
    except ValueError:
        print("Error: Debes ingresar un número entero para el ID del encargado.")
    except Exception as e:
        print(f"Error al eliminar encargado: {e}")
    
    input("\nPresione Enter para continuar...")



############### After Login Handler ###############

def after_login_menu(tipo_usuario):
    if tipo_usuario == "encargado":
        main_menu()
    elif tipo_usuario == "administrador":
        admin_menu()


############### Login ###############

from utils.database import cursor

def verificar_credenciales(usuario, contraseña, tipo_usuario):
    if tipo_usuario == "encargado":
        cursor.execute("SELECT * FROM encargado WHERE correo = %s AND contraseña = %s", (usuario, contraseña))
    elif tipo_usuario == "administrador":
        cursor.execute("SELECT * FROM administrador WHERE correo = %s AND contraseña = %s", (usuario, contraseña))
    
    result = cursor.fetchone()
    return result is not None

def login():
    max_intentos = 3
    intentos = 0
    print("¿Cómo desea iniciar sesión?")
    while intentos < max_intentos:
        tipo_usuario = select_option(["Iniciar sesión como Encargado", "Iniciar sesión como Administrador"])

        usuario = input("Correo: ")
        password = input("Contraseña: ")

        if tipo_usuario == "Iniciar sesión como Encargado":
            if verificar_credenciales(usuario, password, tipo_usuario="encargado"):
                print("Inicio de sesión como Encargado exitoso.")
                return "encargado", usuario
        elif tipo_usuario == "Iniciar sesión como Administrador":
            if verificar_credenciales(usuario, password, tipo_usuario="administrador"):
                print("Inicio de sesión como Administrador exitoso.")
                return "administrador", usuario
        
        intentos += 1
        print(f"Usuario o contraseña incorrectos. Intento {intentos} de {max_intentos}")
        input("Presione Enter para continuar...")
    
    print("Has excedido el número máximo de intentos. Vuelve a iniciar el programa.")
    input("Presione Enter para continuar...")
    clear_console()
    return None, None
