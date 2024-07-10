import msvcrt
import os
from modulos.db import cursor, conexion
from modulos.habitaciones import ag_habitacion, ver_lista_habitaciones
from modulos.pasajeros import registrar_pasajeros, ver_tabla_resumen
from modulos.reserva import registrar_reserva

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
            print(f"> {option}")
        else:
            print(f"  {option}")

def select_option(options, return_index=False):
    selected_index = 0
    while True:
        print_options(options, selected_index)
        key = ord(msvcrt.getch())

        if key == 80:  # Flecha hacia abajo
            selected_index = (selected_index + 1) % len(options)
        elif key == 72:  # Flecha hacia arriba
            selected_index = (selected_index - 1) % len(options)
        elif key == 13:  # Enter
            if return_index:
                return selected_index
            else:
                return options[selected_index]
        elif key == 27:  # Escape
            return None

def print_box():
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 50 + "║")
    print("╚" + "═" * 50 + "╝")

# main menu 
def main_menu():
    options = ["1.- Agregar Habitación", "2.- Registrar Pasajeros", "3.- Mostrar Lista de Habitaciones", "4.- Ver Tabla Resumen de Pasajeros", "5.- Registrar Reserva", "6.- Salir"]
    
    while True:
        clear_console()
        print_box()
        print("MENÚ PRINCIPAL")
        selected_option = select_option(options)
        
        if selected_option == options[0]:
            ag_habitacion()
        elif selected_option == options[1]:
            registrar_pasajeros()
        elif selected_option == options[2]:
            ver_lista_habitaciones()
        elif selected_option == options[3]:
            ver_tabla_resumen()
        elif selected_option == options[4]:
            registrar_reserva()
        elif selected_option == options[5]:
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")
