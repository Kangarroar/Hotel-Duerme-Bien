# main.py
from modulos.terminal import after_login_menu
from modulos.login import login

def main():
    tipo_usuario, usuario = login()
    if tipo_usuario:
        print(f"Bienvenido, {usuario}!")
        after_login_menu(tipo_usuario)
    else:
        print("Inicio de sesión fallido. Vuelve a intentarlo más tarde.")

if __name__ == '__main__':
    main()
