import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QMessageBox,
    QTextEdit,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from pathlib import Path

from logic.Modulo_Files import(
    Path
)
from entities import InstallApp
from data.Modulo_InstallApp import *
from data import Modulo_Language as Lang
from data.interface_data import *

from interface import Modulo_Util_Qt as Util_Qt
from interface.interface_number import *
from interface.css_util import *

data_InstallApp = InstallApp
read_InstallApp( data_InstallApp )


lang = Lang.Language()


class Window_Install(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle(f'{lang["install"]} - {data_InstallApp.name}')
        self.setWindowIcon(QIcon( data_InstallApp.icon ))
        self.resize(nums_win_main[0], nums_win_main[1])
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical - Boton de Información de instalación
        button_info = QPushButton(lang['more_info'])
        button_info.clicked.connect(self.evt_info_install)
        vbox_main.addWidget(button_info)
        
        # Seccion Veritical - Comentario de aplicación
        text_edit = QTextEdit( 
            (
            f'{lang["ver"]} {data_InstallApp.version}\n\n'
            
            f'<b>{data_InstallApp.comment}</b>\n\n'
            ).replace('\n', '<br>')
         )
        text_edit.setReadOnly(True)
        vbox_main.addWidget(text_edit)
        
        # Texto necesario, por si no hay path
        if data_InstallApp.path == '':
            text_dir = Path()
            # Seccion Vertical - Texto de Ayuda
            label = QLabel( lang['set_dir'] )
            vbox_main.addWidget(label)
        else:
            text_dir = data_InstallApp.path
        
        # Seccion Vertical - Separador
        vbox_main.addStretch()
        
        # Seccion Vertical - Directorio
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        self.entry_dir = QLineEdit(
            self,
            maxLength=90,
            placeholderText=lang['dir'],
            clearButtonEnabled=True
        )
        self.entry_dir.setText(text_dir)
        hbox.addWidget(self.entry_dir)
        
        button_dir = QPushButton( lang['set_dir'] )
        button_dir.clicked.connect(self.evt_set_dir)
        hbox.addWidget(button_dir)
        
        # Seccion Vertical - Separador
        vbox_main.addStretch()
        
        # Seccion Vertical - Aceptar
        self.dialog_wait = None
        self.thread_install = None
        button_ok = QPushButton( lang['install'] )
        button_ok.clicked.connect(self.evt_install_files)
        vbox_main.addWidget(button_ok)
        
        # Mostrar Ventana
        self.show()
        
    def evt_info_install(self):
        Util_Qt.Dialog_TextEdit(
            self,
            text = Information( data_InstallApp ), size=nums_win_text_edit
        ).exec()
        
    def evt_set_dir(self):
        dir_name = QFileDialog.getExistingDirectory(
            self,
            lang['set_dir'],                    # Titulo
            self.entry_dir.text()               # Directorio de busqueda
        )
        if dir_name:
            self.entry_dir.setText( str(Path(dir_name)) )
        else:
            pass
        
    def evt_install_files(self):
        self.dialog_wait = Util_Qt.Dialog_Wait(
            self,
            text=lang['help_wait'], size=nums_win_wait
        )
        self.dialog_wait.show()
    
        self.thread_install = Thread_Install( 
            path=self.entry_dir.text()
        )
        self.thread_install.finished.connect( self.install_ready )
        self.thread_install.finished.connect( self.install_dialog )
        self.thread_install.start()
        
    def install_ready(self):
        if self.dialog_wait is not None:
            self.dialog_wait.close()
            self.dialog_wait = None
        
    def install_dialog(self, message):
        # Mostrar mensaje y parar QThread - Hilo
        message_box = QMessageBox(self)
        message_box.setWindowTitle(lang['finalized'])
        message_box.setText(message)
        message_box.exec()
        self.thread_install = None


class Thread_Install(QThread):
    finished = pyqtSignal(str)
    def __init__(self, path='/dir/arch'):
        super().__init__()
        self._path = path

    def run(self):
        message = Install(data_InstallApp, path=self._path)
        
        self.finished.emit(message)




# Estilo de programa y bucle
qss_style = ''
for widget in get_list_text_widget( 'Qt' ):
    if widget == 'QTextEdit':
        qss_style += text_widget_style(
            widget=widget, font=file_font, font_size=num_font, padding=None,
            margin_based_font=False, margin_xy=num_margin_xy, idented=4
        )
    else:
        qss_style += text_widget_style(
            widget=widget, font=file_font, font_size=num_font, padding=num_space_padding,
            margin_based_font=False, margin_xy=num_margin_xy, idented=4
        )
print(qss_style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss_style)
    window = Window_Install()
    sys.exit(app.exec())