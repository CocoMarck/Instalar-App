from pathlib import Path
from Modulos import Modulo_Util as Util
from Modulos import Modulo_InstallApp as InstallApp


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
        Util.Title(f'Install {InstallApp.Name()}')
        text_menu = (
            f'Version: {InstallApp.Version()}\n\n'

            f'{InstallApp.Comment()}\n\n'
            
            f'Ruta de instalación: {path}\n\n'
        )
        option = input(
            text_menu +
            f'3. Mostrar información de instalación\n'
            f'2. Cambiar ruta de instalación\n'
            f'1. Instalar App\n'
            f'0. Salir\n'
            'Elige una opción: '
        )
        
        # Elegir o no la opcion
        option_continue = Util.Continue()
        if option_continue == 's':
            pass
        elif option_continue == 'n':
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
                    Util.Title('Establcer Carpeta', see=False) +
                    'Ruta de carpeta: '
                )
            )

        elif option == '1':
            # Instalar App
            print(
                f'Instalando {InstallApp.Name()}\n'
                'Por favor espere...\n'
            )

            print(InstallApp.Install(path=path) + '\n')

            input('Preciona enter para continuar...')

        elif option == '0':
            # Salir del loop y de la aplicación
            loop = False

        elif option == None:
            # Si no se desa esa opcion enteonces:
            pass

        else:
            # Opcion inexistente
            Util.Continue(txt=option, msg=True)
            
    else:
        # Loop finaliza
        exit()


if __name__ == '__main__':
    Install_Menu()