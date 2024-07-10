from modulos.terminal import main_menu
from modulos.login import login

def main():
    login_success = login()
    if login_success:
        main_menu()
    else:
        return

if __name__ == '__main__':
    main()
