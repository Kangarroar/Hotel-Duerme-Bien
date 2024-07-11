import msvcrt
import os
from utils.roomsmanager import registrar_reserva, ver_lista_habitaciones, ag_habitacion
from utils.pasajeros import registrar_pasajeros, ver_tabla_resumen
# limpiador
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# error handler numerico


# error handler hipercaracteres


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


# Menú principal
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
# Menú para el administrador
def admin_menu():
    add_encargado_option = '1.- Agregar encargado'
    delete_encargado_option = '2.- Eliminar encargado'
    back_option = '3.- Volver atrás'
    options = [add_encargado_option, delete_encargado_option, back_option]

    while True:
        selected_option = select_option(options)

        if selected_option == add_encargado_option:
            print("Opción para agregar encargado seleccionada.")
            # Lógica para agregar encargado
            input("Presione Enter para continuar...")
        elif selected_option == delete_encargado_option:
            print("Opción para eliminar encargado seleccionada.")
            # Lógica para eliminar encargado
            input("Presione Enter para continuar...")
        elif selected_option == back_option:
            return


def after_login_menu(tipo_usuario):
    if tipo_usuario == "encargado":
        main_menu()
    elif tipo_usuario == "administrador":
        admin_menu()

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
    print("Como desea iniciar sesion?")
    while intentos < max_intentos:
        tipo_usuario = select_option(["Encargado", "Administrador"])

        usuario = input("Usuario: ")
        password = input("Contraseña: ")

        if tipo_usuario == "Encargado":
            if verificar_credenciales(usuario, password, tipo_usuario="encargado"):
                print("Inicio de sesión como Encargado exitoso.")
                return "encargado", usuario
        elif tipo_usuario == "Administrador":
            if verificar_credenciales(usuario, password, tipo_usuario="administrador"):
                print("Inicio de sesión como Administrador exitoso.")
                return "administrador", usuario
        
        intentos += 1
        print(f"Usuario o contraseña incorrectos. Intento {intentos} de {max_intentos}")
    
    print("Has excedido el número máximo de intentos. Vuelve a iniciar el programa.")
    return None, None