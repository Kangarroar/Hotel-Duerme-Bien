from utils.terminal import print_box, login, after_login_menu

def main():
    print_box()
    tipo_usuario, usuario = login()
    if tipo_usuario:
        after_login_menu(tipo_usuario)
if __name__ == '__main__':
    main()
