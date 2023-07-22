from pathlib import Path
from Modulos import Modulo_Util as Util
from Modulos import Modulo_InstallApp as InstallApp
from Modulos.Modulo_Language import (
    YesNo,
    get_text as Lang
)

from Modulos.Modulo_ShowPrint import (
    Continue,
    Title
)


def Install_Menu():
    # Verificar que exista el texto del path
    if InstallApp.Path() == '':
        path = Util.Path()
    else:
        path = InstallApp.Path()

    # Loop de Opciones
    loop = True
    while loop == True:
        # Opciones
        Util.CleanScreen()
        Title(f'{Lang("install")} {InstallApp.Name()}')
        text_menu = (
            f'{Lang("ver")}: {InstallApp.Version()}\n\n'

            f'{InstallApp.Comment()}\n\n'
            
            f'{Lang("dir")}: {path}\n\n'
        )
        option = input(
            text_menu +
            f'3. {Lang("more_info")}\n'
            f'2. {Lang("set_dir")}\n'
            f'1. {Lang("install")}\n'
            f'0. {Lang("exit")}\n'
            f'{Lang("set_option")}: '
        )
        
        # Elegir o no la opcion
        option_continue = Continue()
        if option_continue == YesNo('yes'):
            pass
        elif option_continue == YesNo('no'):
            option = None
        
        # Opcion elegida
        Util.CleanScreen()
        if option == '3':
            # Mostrar Información de instalacion
            input(InstallApp.Information())
                
        
        elif option == '2':
            # Cambiar ruta de instalación
            path = Util.Path(
                input(
                    Title(Lang('set_dir'), print_mode=False) +
                    f'{Lang("dir")}: '
                )
            )

        elif option == '1':
            # Instalar App
            Title(f'{Lang("install")} {InstallApp.Name()}')
            print(
                f'{Lang("help_wait")}...\n'
            )

            print(InstallApp.Install(path=path) + '\n')

            input(f'{Lang("continue_enter")}...')

        elif option == '0':
            # Salir del loop y de la aplicación
            loop = False

        elif option == None:
            # Si no se desa esa opcion enteonces:
            pass

        else:
            # Opcion inexistente
            Continue(text=option, message_error=True)
            
    else:
        # Loop finaliza
        pass


if __name__ == '__main__':
    Install_Menu()