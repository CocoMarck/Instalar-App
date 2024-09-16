from pathlib import Path as pathlib

from entities import InstallApp
from logic.Modulo_Text import (
    Ignore_Comment,
    Text_Read,
    Text_Separe
)
from logic.Modulo_Files import(
    Files_List,
    Files_Copy,
    Create_Dir,
    Execute_DirectAccess
)
from logic.Modulo_System import(
    View_echo,
)
from data.Modulo_Language import Language

import sys, os

# Obtén la ruta al directorio actual del script
current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )

# Construye la ruta a Languages desde el directorio que contiene el módulo
dir_data = os.path.join(current_dir, 'Install-App_resources')

# Archivo de registro de configuraciónes
install_app_dat = os.path.join( dir_data, 'Install-App.dat' )


lang = Language()


# Leer datos del texto de instalación
text_installer = Ignore_Comment(
        text=Text_Read(
            file_and_path=install_app_dat,
            option='ModeText'
        ),
        comment='#'
    )

# Separarar datos del texto de instalacion, sobre caracteres '='
text_dict = Text_Separe(
        text=text_installer,
        text_separe='='
    )
    
# Agregar Informacion del texto de instalacion, en las variables
def Path():
    return View_echo(text=text_dict['path'])

# Version de aplicación
def Version():
    return float(text_dict['version'])

# Aplicacion a ejecutar
def Exec():
    return text_dict['exec']

# Nombre de aplicación
def Name():
    return text_dict['name']

# Icono de aplicacion
def Icon():
    return text_dict['icon']

# Comentario
def Comment():
    return text_dict['comment']

# Abir o no en Terminal
def Terminal():
    terminal = text_dict['terminal']
    if terminal == 'True':
        terminal = True
    elif terminal == 'False':
        terminal = False
    else:
        terminal = False

    return terminal

# Categorias
def Categories():
    categories = text_dict['categories']
    categories_list = []
    for categorie in categories.split(','):
        categories_list.append(categorie)
    categories = categories_list
    
    return categories_list


def Install(InstallApp, path=''):
    '''Instalar App a una ruta establecida'''
    try:
        # Crear Carpeta, si es que no existe
        Create_Dir( path )
        # Si existe la carpeta entonces
        if pathlib( path ).exists():
            # Lista de archivos
            file_list = Files_List(
                files = '*',
                path = './',
                remove_path = False,
            )
            # Excluir de la lista de archivos
            exclude_installer = Files_List(
                files = 'Install-App*',
                path = './',
                remove_path = False
            )
            for exclude in exclude_installer:
                file_list.remove(exclude)
            
            # Copiar Archivos a la ruta asignada
            for file_ready in file_list:
                Files_Copy( 
                    file_ready, # Archivo
                    path # Ruta
                )
                
            # Crear acceso directo
            Execute_DirectAccess(
                version=InstallApp.version,
                path=InstallApp.path,
                name=InstallApp.name,
                execute=InstallApp.exec,
                icon=InstallApp.icon,
                comment=InstallApp.comment,
                terminal=InstallApp.terminal,
                categories=InstallApp.categories
            )
            
            # Mensaje indicador de finalizacion
            message = lang['fin_install']
        
        else:
            message = f'ERROR - {lang["error_dir"]}'
    except:
        message = (
            'ERROR\n'
            f'- {lang["error_admin"]}\n'
            f'- {lang["error_parameter"]}'
        )
    
    return message


def Information( InstallApp ):
    '''Mostrar información de instalación'''
    return(
        f'{lang["ver"]}: { InstallApp.version }\n\n'
    
        f'{lang["dir"]}: { InstallApp.path }\n\n'
    
        f'{lang["name"]}: { InstallApp.name }\n\n'

        f'{lang["exec"]}: { InstallApp.exec }\n\n'
        
        f'{lang["icon"]}: { InstallApp.icon }\n\n'
        
        f'{lang["comment"]}: { InstallApp.comment }\n\n'

        f'{lang["terminal"]}: { InstallApp.terminal }\n\n'

        f'{lang["categories"]}: { InstallApp.categories }'
    )




def read_InstallApp( InstallApp ):
    '''Leer archivo y establecer parametros en la entidad InstallApp'''
    InstallApp.version = Version()
    InstallApp.path = Path()
    InstallApp.name = Name()
    InstallApp.exec = Exec()
    InstallApp.icon = Icon()
    InstallApp.comment = Comment()
    InstallApp.terminal = Terminal()
    InstallApp.categories = Categories()