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
        self.boton_iniciar.clicked.connect(self.ingresaredf)
        self.boton_salir.clicked.connect(lambda:self.close())

    def ingresaredf(self):
        ventana_ruta = Rutaedf(self)
        self.hide()
        ventana_ruta.asignarControlador(self.__mi_controlador)
        ventana_ruta.show()
        
    def asignarControlador(self, c):
        self.__mi_controlador = c

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
        self.edf = self.edf.text()
        self.mostraredf= self.__mi_controlador.lectoredf(self.edf)
        self.convertedf = self.__mi_controlador.convertedf(self.edf,self.dicom)
        ventana_ver = MostrarNifti(self)
        self.hide()
        ventana_ver.asignarControlador(self.__mi_controlador)
        ventana_ver.show()
    def devolver(self):
        self.__ventanapadre.show()
        self.hide()

    def asignarControlador(self, c):
        self.__mi_controlador = c


class MostrarNifti(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__ventanapadre=parent
        self.setup
    def setup (self):
        self.Mostrar.clicked.connect(self.Nifti)
        self.volver.clicked.connect(self.devolver)
    def Nifti (self):
        self.dicom= self.__mi_controlador.cargardicom(self.dicom)
        self.convertdicom= self.__mi_controlador.convertdicom(self.dicom)
        self.carpetaNueva = './nifti'
        for archivo in os.listdir(self.carpetaNueva):
          if archivo.endswith('.nii.gz'):
            self.ruta = os.path.join(self.carpetaNueva,archivo)
            malla = Volume(self.ruta)
            malla.mode(1).cmap("red") 
            plt = RayCastPlotter(malla, axes=7)
            show(malla, zoom=1.2, bg="blue", viewup="z").close() 
            self.hide()
            self.__ventanapadre.show()
    def devolver(self):
        self.__ventanapadre.show()
        self.hide()
    def asignarControlador(self, c):
        self.__mi_controlador = c
    