from modulos.terminal import print_box
from modulos.db import verificar_credenciales

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
