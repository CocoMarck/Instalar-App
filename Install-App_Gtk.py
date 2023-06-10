import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from pathlib import Path
import threading
import Modulo_Util as Util
import Modulo_Util_Gtk as Util_Gtk


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
path = Util.View_echo(text=text_dict['path'])
if path == '':
    go = False
else:
    go = True

# Version de aplicación
app_version = float(text_dict['version'])

# Aplicacion a ejecutar
app_exec = text_dict['exec']

# Nombre de aplicación
app_name = text_dict['name']

# Icono de aplicacion
app_icon = text_dict['icon']

# Comentario
comment = text_dict['comment']

# Abir o no en Terminal
terminal = text_dict['terminal']
if terminal == 'True':
    terminal = True
elif terminal == 'False':
    terminal = False
else:
    terminal = False

# Categorias
categories = text_dict['categories']
categories_list = []
for categorie in categories.split(','):
    categories_list.append(categorie)
categories = categories_list


class Window_Install(Gtk.Window):
    def __init__(self):
        super().__init__(title=f'Install {app_name}')
        self.set_resizable(True)
        self.set_default_size(512, 256)
        self.set_icon_from_file(app_icon)
        
        # Contenedor principal - VBox
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Seccion Veritcal - Boton de Información adicional
        button_info = Gtk.Button(label='Mostrar mas información')
        button_info.connect('clicked', self.evt_info_install)
        vbox_main.pack_start(button_info, False, False, 0)
        
        # Seccion Vertical - Text View Comentario de eplicacion
        text_scroll = Gtk.ScrolledWindow()
        text_scroll.set_hexpand(True)
        text_scroll.set_vexpand(True)
        
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_editable(False)

        text_buffer = text_view.get_buffer()
        text_buffer.set_text(
            f'Versión {app_version}\n\n'

            f'{comment}\n\n'
        )

        text_scroll.add(text_view)
        
        vbox_main.pack_start(text_scroll, True, True, 0)
        
        # Texto de ayuda
        if go == True:
            text_dir = path
        else:
            text_dir = Util.Path()
            # Seccion Vertical - Texto de Ayuda
            label = Gtk.Label(label='Establece un directorio')
            vbox_main.pack_start(label, True, False, 0)
        
        # Seccion Vertical - Directorio
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, False, False, 8 )
        
        self.entry_dir = Gtk.Entry()
        self.entry_dir.set_placeholder_text('Establece un directorio')
        self.entry_dir.set_hexpand(True)
        self.entry_dir.set_text(text_dir)
        hbox.pack_start(self.entry_dir, True, True, 0)
        
        button_dir = Gtk.Button(label='Elegir ruta')
        button_dir.connect('clicked', self.evt_set_dir)
        hbox.pack_end(button_dir, False, False, 0)
        
        # Seccion Vertical - Boton aceptar
        #self.dialog_wait = None
        #self.thread = None
        button_ok = Gtk.Button(label='Instalar App')
        button_ok.connect('clicked', self.evt_install_files)
        vbox_main.pack_end(button_ok, False, False, 0)
        
        # Fin, Agregar Contenedor principal
        self.add(vbox_main)
        
    def evt_info_install(self, widget):
        dialog = Util_Gtk.Dialog_TextView(
            self,
            text=(
                f'Versión: {app_version}\n\n'
            
                f'Ruta de instalacion por defecto: {path}\n\n'
            
                f'Nombre de aplicación: {app_name}\n\n'

                f'Aplicación a ejecutar: {app_exec}\n\n'
                
                f'Icono: {app_icon}\n\n'
                
                f'Comentario de aplicación: {comment}\n\n'

                f'Ejecutar por terminal: {terminal}\n\n'

                f'Lista de categorias: {categories}'
            )
        )
        dialog.run()
        dialog.destroy()
        
    def evt_set_dir(self, widget):
        dialog = Gtk.FileChooserDialog(
            parent=self,
            title='Select one Folder',
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            'Select',
            Gtk.ResponseType.OK
        )
        dialog.set_current_folder( self.entry_dir.get_text() )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.entry_dir.set_text( dialog.get_filename() )
        elif response == Gtk.ResponseType.CANCEL:
            pass
            
        dialog.destroy()
        
    def evt_install_files(self, widget):
        self.dialog_wait = Util_Gtk.Dialog_Wait(
            self, text='Por favor espera...\n'
        )

        # Hilo - Subproceso para que no se conjele el loop de la app
        self.thread = threading.Thread(target=self.thread_install)
        self.thread.start()
        
        self.dialog_wait.run()
    
    def thread_install(self):
        try:
            # Crear Carpeta, si es que no existe
            Util.Create_Dir( self.entry_dir.get_text() )
            # Si existe la carpeta entonces
            if Path( self.entry_dir.get_text() ).exists():
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
                        self.entry_dir.get_text() # Ruta
                    )
                    
                # Crear acceso directo
                Util.Execute_DirectAccess(
                    version=app_version,
                    path=self.entry_dir.get_text(),
                    name=app_name,
                    execute=app_exec,
                    icon=app_icon,
                    comment=comment,
                    terminal=terminal,
                    categories=categories
                )
                
                # Mensaje indicador de finalizacion
                self.message = 'Instalacion Satisfactoria'
            
            else:
                self.message ='ERROR - Directorio incorrecto.'
        except:
            self.message = (
                'ERROR\n'
                'El programa necesita permisos de administrador.\n'
                'O algun parametro es incorrecto.'
            )
        
        GLib.idle_add(self.thread_install_finish)
    
    def thread_install_finish(self):
        self.dialog_wait.destroy()
        #self.dialog_wait = None
    
        dialog_message = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=self.message
        )
        dialog_message.run()
        dialog_message.destroy()


win = Window_Install()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()