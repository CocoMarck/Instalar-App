from pathlib import Path as pathlib

from .Modulo_Text import (
    Ignore_Comment,
    Text_Read,
    Text_Separe
)
from .Modulo_Files import(
    Files_List,
    Files_Copy,
    Create_Dir,
    Execute_DirectAccess
)
from .Modulo_System import(
    View_echo,
)
from .Modulo_Language import Language


lang = Language()


# Leer datos del texto de instalación
text_installer = Ignore_Comment(
        text=Text_Read(
            file_and_path='./Install-App.dat',
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


def Install(path=''):
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
                version=Version(),
                path=path,
                name=Name(),
                execute=Exec(),
                icon=Icon(),
                comment=Comment(),
                terminal=Terminal(),
                categories=Categories()
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


def Information():
    '''Mostrar información de instalación'''
    return(
        f'{lang["ver"]}: {Version()}\n\n'
    
        f'{lang["dir"]}: {Path()}\n\n'
    
        f'{lang["name"]}: {Name()}\n\n'

        f'{lang["exec"]}: {Exec()}\n\n'
        
        f'{lang["icon"]}: {Icon()}\n\n'
        
        f'{lang["comment"]}: {Comment()}\n\n'

        f'{lang["terminal"]}: {Terminal()}\n\n'

        f'{lang["categories"]}: {Categories()}'
    )