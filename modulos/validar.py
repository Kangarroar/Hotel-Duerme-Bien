import datetime
import re
# Función para validar input numérico
def validar_numero(input_str):
    while True:
        try:
            numero = int(input_str)
            return numero
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            input_str = input("Introduce nuevamente: ")

# Función para validar input de fecha
def validar_fecha(input_str):
    while True:
        try:
            fecha = datetime.strptime(input_str, "%Y-%m-%d").date()
            return fecha
        except ValueError:
            print("Error: Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
            input_str = input("Introduce nuevamente: ")

# Función para validar input de correo electrónico
def validar_correo(input_str):
    while True:
        if re.match(r"[^@]+@[^@]+\.[^@]+", input_str):
            return input_str
        else:
            print("Error: Formato de correo electrónico inválido.")
            input_str = input("Introduce nuevamente: ")

# Función para validar input de teléfono
def validar_telefono(input_str):
    while True:
        if re.match(r"^[\d+\s]*$", input_str):
            return input_str
        else:
            print("Error: El número de teléfono debe contener solo dígitos y espacios.")
            input_str = input("Introduce nuevamente: ")

# Función para validar input de RUT
def validar_rut(input_str):
    while True:
        if re.match(r"^(\d{7,8})-([\dkK])$", input_str):
            return input_str
        else:
            print("Error: Formato de RUT inválido.")
            input_str = input("Introduce nuevamente: ")
