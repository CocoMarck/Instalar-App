import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import threading

from logic.Modulo_Files import(
    Path
)
from entities import InstallApp
from data.Modulo_InstallApp import *
from data.Modulo_Language import Language
from interface import Modulo_Util_Gtk as Util_Gtk

data_InstallApp = InstallApp
read_InstallApp( data_InstallApp )


lang = Language()


class Window_Install(Gtk.Window):
    def __init__(self):
        super().__init__(
            title=f'{lang["install"]} - {data_InstallApp.name}'
        )
        self.set_resizable(True)
        self.set_default_size(512, 256)
        self.set_icon_from_file( data_InstallApp.icon )
        
        # Contenedor principal - VBox
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Seccion Veritcal - Boton de Información adicional
        button_info = Gtk.Button( label=lang['more_info'] )
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
            f'{lang["ver"]} {data_InstallApp.version}\n\n'

            f'{data_InstallApp.comment}\n\n'
        )

        text_scroll.add(text_view)
        
        vbox_main.pack_start(text_scroll, True, True, 0)
        
        # Texto de ayuda, por si no hay path
        if data_InstallApp.path == '':
            text_dir = Path()
            # Seccion Vertical - Texto de Ayuda
            label = Gtk.Label( label=lang['set_dir'] )
            vbox_main.pack_start(label, True, False, 0)
        else:
            text_dir = data_InstallApp.path
        
        # Seccion Vertical - Directorio
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, False, False, 8 )
        
        self.entry_dir = Gtk.Entry()
        self.entry_dir.set_placeholder_text( lang['dir'] )
        self.entry_dir.set_hexpand(True)
        self.entry_dir.set_text(text_dir)
        hbox.pack_start(self.entry_dir, True, True, 0)
        
        button_dir = Gtk.Button( label=lang['set_dir'] )
        button_dir.connect('clicked', self.evt_set_dir)
        hbox.pack_end(button_dir, False, False, 0)
        
        # Seccion Vertical - Boton aceptar
        #self.dialog_wait = None
        #self.thread = None
        button_ok = Gtk.Button( label=lang['install'] )
        button_ok.connect('clicked', self.evt_install_files)
        vbox_main.pack_end(button_ok, False, False, 0)
        
        # Fin, Agregar Contenedor principal
        self.add(vbox_main)
        
    def evt_info_install(self, widget):
        dialog = Util_Gtk.Dialog_TextView(
            self,
            text=Information( data_InstallApp )
        )
        dialog.run()
        dialog.destroy()
        
    def evt_set_dir(self, widget):
        dialog = Gtk.FileChooserDialog(
            parent=self,
            title=lang['set_dir'],
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            lang['set_dir'],
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
            self, text=lang['wait']
        )

        # Hilo - Subproceso para que no se conjele el loop de la app
        self.thread = threading.Thread(target=self.thread_install)
        self.thread.start()
        
        self.dialog_wait.run()
    
    def thread_install(self):
        self.message = Install(
            data_InstallApp,
            path=self.entry_dir.get_text()
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