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
import Modulo_Util as Util
import Modulo_Util_Qt as Util_Qt
import Modulo_InstallApp as InstallApp


class Window_Install(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle(f'Install - {InstallApp.Name()}')
        self.setWindowIcon(QIcon( InstallApp.Icon() ))
        self.setGeometry(100, 100, 512, 256)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical - Boton de Información de instalación
        button_info = QPushButton('Mostrar mas Información')
        button_info.clicked.connect(self.evt_info_install)
        vbox_main.addWidget(button_info)
        
        # Seccion Veritical - Comentario de aplicación
        text_edit = QTextEdit( 
            (
            f'Versión {InstallApp.Version()}\n\n'
            
            f'<b>{InstallApp.Comment()}</b>\n\n'
            ).replace('\n', '<br>')
         )
        text_edit.setReadOnly(True)
        vbox_main.addWidget(text_edit)
        
        # Texto necesario, por si no hay path
        if InstallApp.Path() == '':
            text_dir = Util.Path()
            # Seccion Vertical - Texto de Ayuda
            label = QLabel('Establece un Directorio')
            vbox_main.addWidget(label)
        else:
            text_dir = InstallApp.Path()
        
        # Seccion Vertical - Separador
        vbox_main.addStretch()
        
        # Seccion Vertical - Directorio
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        self.entry_dir = QLineEdit(
            self,
            maxLength=90,
            placeholderText='Establece el Directorio',
            clearButtonEnabled=True
        )
        self.entry_dir.setText(text_dir)
        hbox.addWidget(self.entry_dir)
        
        button_dir = QPushButton('Elegir Ruta')
        button_dir.clicked.connect(self.evt_set_dir)
        hbox.addWidget(button_dir)
        
        # Seccion Vertical - Separador
        vbox_main.addStretch()
        
        # Seccion Vertical - Aceptar
        self.dialog_wait = None
        self.thread_install = None
        button_ok = QPushButton('Instalar App')
        button_ok.clicked.connect(self.evt_install_files)
        vbox_main.addWidget(button_ok)
        
        # Mostrar Ventana
        self.show()
        
    def evt_info_install(self):
        Util_Qt.Dialog_TextEdit(
            self,
            text = InstallApp.Information()
        ).exec()
        
    def evt_set_dir(self):
        dir_name = QFileDialog.getExistingDirectory(
            self,
            'Seleccionar Diractorio/Carpeta',   # Titulo
            self.entry_dir.text()               # Directorio de busqueda
        )
        if dir_name:
            self.entry_dir.setText( str(Path(dir_name)) )
        else:
            pass
        
    def evt_install_files(self):
        self.dialog_wait = Util_Qt.Dialog_Wait(
            self,
            text='Por favor, espere...'
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

        self.thread_install = None
        
    def install_dialog(self, message):
        message_box = QMessageBox(self)
        message_box.setWindowTitle('Install Complete')
        message_box.setText(message)
        message_box.exec()


class Thread_Install(QThread):
    finished = pyqtSignal(str)
    def __init__(self, path='/Ruta/Necesaria'):
        super().__init__()
        self._path = path

    def run(self):
        message = InstallApp.Install(path=self._path)
        
        self.finished.emit(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Install()
    sys.exit(app.exec())