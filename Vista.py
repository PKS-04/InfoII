import json
import os
from vedo import Volume, show
from vedo.applications import RayCastPlotter
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QLineEdit, QTableWidgetItem
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import  QRegExp, Qt
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Ppal(QMainWindow):
    def __init__(self):
        super(Ppal, self).__init__()
        loadUi("InfoII\Ppal.ui",self)
        self.setup()

    def setup(self):
        self.boton_iniciaredf.clicked.connect(self.rutaedf)
        self.boton_iniciarnifti.clicked.connect(self.rutanifti)
        self.boton_salir.clicked.connect(lambda:self.close())

    def rutaedf(self):
            ventedf = Rutaedf(self)
            ventedf.asignarControlador(self.__mi_controlador)
            ventedf.show()
            self.hide()
    def rutanifti(self):
        ventMenu =  MostrarNifti(self)
        ventMenu.asignarControlador(self.__mi_controlador)
        ventMenu.show()
        self.hide()
        
    def asignarControlador(self, c):
        self.__mi_controlador = c
class VentanaMenu(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi("Menu.ui",self)
        self.__ventana_padre=parent
        self.setup()

    def setup(self):
        self.boton_imagenes.clicked.connect(self.rutaedf)
        
        self.boton_salir.clicked.connect(lambda:self.close())

    def rutaedf(self):
            ventedf = Rutaedf(self)
            ventedf.asignarControlador(self.__mi_controlador)
            ventedf.show()
            self.hide()
    
    
    def asignarControlador(self, c):
        self.__mi_controlador = c

    

    

    def volverBoton(self):
        self.__ventana_padre.show()
        self.hide()

class Rutaedf(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi("InfoII\Rutaedf.ui",self)
        self.__ventanapadre=parent
        self.dicom = None
        self.setup()
        
    def setup (self):
        self.Ingresar.clicked.connect(self.rutaedf)
        self.Volver.clicked.connect(self.devolver)
    def rutaedf(self):
        try:
            self.ruta_edf = self.edf.text() 
            self.cargo = self.__mi_controlador.lectoredf(self.ruta_edf)
            self.carpetaedf = './edf'
            for archivo in os.listdir(self.carpetaedf):
                if archivo.endswith('.edf'):
                    self.ruta_edf = os.path.join(self.carpetaedf,archivo)
                    self.cargo = self.__mi_controlador.lectoredf(self.ruta_edf)
                else:
                    QMessageBox.critical(self, "Error", f"No se encuentra el archivo: {e}")
            self.hide() 
            self.__ventanapadre.show()      
        except Exception as e:  
                QMessageBox.critical(self, "Error", f"Error al procesar el archivo: {e}")
               
    def devolver(self):
        self.__ventanapadre.show()
        self.hide()

    def asignarControlador(self, c):
        self.__mi_controlador = c


class MostrarNifti(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi("InfoII\MostarNifti.ui",self)
        self.__ventanapadre=parent
        self.setup()

    def asignarControlador(self,c):
        self.__mi_controlador = c

    def setup(self):
        self.Ingresar.clicked.connect(self.rutaImagenNifti)
        self.volver.clicked.connect(self.volverBoton)

    def rutaImagenNifti(self):
        self.ruta = self.nifti.text()
        malla = Volume(self.ruta)
        malla.mode(1).cmap("cold_hot") 
        plt = RayCastPlotter(malla, axes=7)
        show(malla, zoom=1.22, bg="blue", viewup="z").close() 
        self.close()
        self.__ventanapadre.show()
    def volverBoton(self):
        self.__ventanapadre.show()
        self.hide()
    