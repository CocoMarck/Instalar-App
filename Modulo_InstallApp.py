from pathlib import Path as pathlib
import Modulo_Util as Util


# Leer datos del texto de instalación
text_installer = Util.Ignore_Comment(
        text=Util.Text_Read(
            file_and_path='./Install-App.dat',
            opc='ModeText'
        ),
        comment='#'
    )

# Separarar datos del texto de instalacion, sobre caracteres '='
text_dict = Util.Text_Separe(
        text=text_installer,
        text_separe='='
    )
    
# Agregar Informacion del texto de instalacion, en las variables
def Path():
    return Util.View_echo(text=text_dict['path'])

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
        Util.Create_Dir( path )
        # Si existe la carpeta entonces
        if pathlib( path ).exists():
            # Lista de archivos
            file_list = Util.Files_List(
                files = '*',
                path = './',
                remove_path = False,
            )
            # Excluir de la lista de archivos
            exclude_installer = Util.Files_List(
                files = 'Install-App*',
                path = './',
                remove_path = False
            )
            for exclude in exclude_installer:
                file_list.remove(exclude)
            
            # Copiar Archivos a la ruta asignada
            for file_ready in file_list:
                Util.Files_Copy( 
                    file_ready, # Archivo
                    path # Ruta
                )
                
            # Crear acceso directo
            Util.Execute_DirectAccess(
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
            message = 'Instalacion Satisfactoria'
        
        else:
            message ='ERROR - Directorio incorrecto.'
    except:
        message = (
            'ERROR\n'
            'El programa necesita permisos de administrador.\n'
            'O algun parametro es incorrecto.'
        )
    
    return message


def Information():
    '''Mostrar información de instalación'''
    return(
        f'Versión: {Version()}\n\n'
    
        f'Ruta de instalacion por defecto: {Path()}\n\n'
    
        f'Nombre de aplicación: {Name()}\n\n'

        f'Aplicación a ejecutar: {Exec()}\n\n'
        
        f'Icono: {Icon()}\n\n'
        
        f'Comentario de aplicación: {Comment()}\n\n'

        f'Ejecutar por terminal: {Terminal()}\n\n'

        f'Lista de categorias: {Categories()}'
    )