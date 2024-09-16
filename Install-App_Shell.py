from pathlib import Path
from entities.InstallApp import *
from data.Modulo_InstallApp import *

from logic.Modulo_System import (
    CleanScreen
)

from logic.Modulo_Files import(
    Path
)
from data.Modulo_Language import (
    YesNo,
    get_text as Lang
)

from interface.Modulo_ShowPrint import (
    Continue,
    Title
)

data_InstallApp = InstallApp
read_InstallApp( data_InstallApp )




def Install_Menu():
    # Verificar que exista el texto del path
    if data_InstallApp.path == '':
        path = Path()
    else:
        path = data_InstallApp.path

    # Loop de Opciones
    loop = True
    while loop == True:
        # Opciones
        CleanScreen()
        Title(f'{Lang("install")} {data_InstallApp.name}')
        text_menu = (
            f'{Lang("ver")}: {data_InstallApp.version}\n\n'

            f'{data_InstallApp.comment}\n\n'
            
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
        CleanScreen()
        if option == '3':
            # Mostrar Información de instalacion
            input( Information(data_InstallApp) )
                
        
        elif option == '2':
            # Cambiar ruta de instalación
            path = Path(
                input(
                    Title(Lang('set_dir'), print_mode=False) +
                    f'{Lang("dir")}: '
                )
            )

        elif option == '1':
            # Instalar App
            Title(f'{Lang("install")} {data_InstallApp.name}')
            print(
                f'{Lang("help_wait")}...\n'
            )

            print( Install(data_InstallApp, path=path) + '\n')

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