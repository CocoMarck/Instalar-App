import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QMessageBox,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt
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
        #self.setWindowIcon(QIcon('/Ruta/Icono.png'))
        self.setGeometry(100, 100, 512, 256)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical - Boton de Información de instalación
        button_info = QPushButton('Mostrar Información de instalación')
        button_info.clicked.connect(self.evt_info_install)
        vbox_main.addWidget(button_info)
        
        # Texto necesario
        if go == True:
            text_help = 'Directorio Establecido'
            text_dir = path
        else:
            text_help = 'Establece un Directorio'
            text_dir = Util.Path()
        
        # Seccion Vertical - Texto de Ayuda
        label = QLabel()
        label.setText(text_help)
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
        
        hbox.addStretch()
        
        button_dir = QPushButton('Elegir Ruta')
        button_dir.clicked.connect(self.evt_set_dir)
        hbox.addWidget(button_dir)
        
        # Seccion Vertical - Separador
        vbox_main.addStretch()
        
        # Seccion Vertical - Aceptar
        button_ok = QPushButton('Instalar App')
        button_ok.clicked.connect(self.evt_copy_files)
        vbox_main.addWidget(button_ok)
        
        # Mostrar Ventana
        self.show()
        
    def evt_info_install(self):
        Util_Qt.Dialog_TextEdit(
            self,
            text = (
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
        
    def evt_copy_files(self):
        dialog_wait = Util_Qt.Dialog_Wait(self, text='Por favor espera...')
        dialog_wait.show()
        
        # Crear Carpeta, si es que no existe
        Util.Create_Dir( self.entry_dir.text() )
        # Si existe la carpeta entonces
        if Path( self.entry_dir.text() ).exists():
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
                    self.entry_dir.text() # Ruta
                )
                
            # Crear acceso directo
            Util.App_DirectAccess(
                path=self.entry_dir.text(),
                name=app_name,
                app_exec=app_exec,
                icon=app_icon,
                comment=comment,
                terminal=terminal,
                categories=categories
            )
            
            dialog_wait.close()
            # Mensaje indicador de finalizacion
            QMessageBox.information(
                self,
                'Install Complete',
                
                'Listo, aplicación instalada'
            )
        else:
            dialog_wait.close()
            QMessageBox.critical(
                self,
                'Error - Dir',
                
                'ERROR\n'
                'No existe el directorio.\n'
                'Establece un Directorio correcto.\n\n'
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Install()
    sys.exit(app.exec())