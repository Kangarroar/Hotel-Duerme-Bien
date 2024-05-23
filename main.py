from modulos.func import *
import modulos.db

def main():
    login_success = login()
    if login_success:
        main_menu()
    else:
        return

if __name__ == '__main__':
    main()
