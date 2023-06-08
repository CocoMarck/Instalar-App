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


class Window_Install(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle(f'Install - {app_name}')
        self.setWindowIcon(QIcon(app_icon))
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
            f'Versión {app_version}\n\n'
            
            f'<b>{comment}</b>\n\n'
            ).replace('\n', '<br>')
         )
        text_edit.setReadOnly(True)
        vbox_main.addWidget(text_edit)
        
        # Texto necesario
        if go == True:
            text_dir = path
        else:
            text_dir = Util.Path()
            # Seccion Vertical - Texto de Ayuda
            label = QLabel('Establece un Directorio')
            vbox_main.addWidget(label)
        
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
            text = (
                f'<b>Versión:</b> {app_version}\n\n'
            
                f'<b>Ruta de instalacion por defecto:</b> {path}\n\n'
            
                f'<b>Nombre de aplicación:</b> {app_name}\n\n'

                f'<b>Aplicación a ejecutar:</b> {app_exec}\n\n'
                
                f'<b>Icono:</b> {app_icon}\n\n'
                
                f'<b>Comentario de aplicación:</b> {comment}\n\n'

                f'<b>Ejecutar por terminal:</b> {terminal}\n\n'

                f'<b>Lista de categorias:</b> {categories}'
            )
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
    def __init__(self, path=path):
        super().__init__()
        self._path = path

    def run(self):
        try:
            # Crear Carpeta, si es que no existe
            Util.Create_Dir( self._path )
            # Si existe la carpeta entonces
            if Path( self._path ).exists():
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
                        self._path # Ruta
                    )
                    
                # Crear acceso directo
                Util.Execute_DirectAccess(
                    version=app_version,
                    path=self._path,
                    name=app_name,
                    execute=app_exec,
                    icon=app_icon,
                    comment=comment,
                    terminal=terminal,
                    categories=categories
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
        
        self.finished.emit(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Install()
    sys.exit(app.exec())