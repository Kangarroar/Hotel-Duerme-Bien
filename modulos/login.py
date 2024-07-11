from modulos.terminal import print_box, select_option
from modulos.db import verificar_credenciales

def login():
    max_intentos = 3
    intentos = 0
    
    while intentos < max_intentos:
        print_box()
        print("Iniciar sesión\n")
        print("Selecciona el tipo de usuario:")
        tipo_usuario = select_option(["Encargado", "Administrador"])

        usuario = input("Usuario: ")
        password = input("Contraseña: ")

        # Verificar el usuario y la contraseña en la base de datos según el tipo de usuario
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