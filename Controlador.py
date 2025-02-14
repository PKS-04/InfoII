from Modelo import EDF,DICOM,Imagen
from Vista import Ppal
from PyQt5.QtWidgets import QApplication
import sys

class Controlador(object):
    def __init__ (self,vista,edf,dicom):
        self.__mi_vista=vista
        self.__mi_edf=edf
        self.__mi_dicom=dicom
    def lectoredf(self,edf):
        return self.__mi_edf.lector_mostraredf(edf)
    def convertedf(self, edf,dicom):
        return self.__mi_edf.convertedf(edf,dicom) 
    
    def leerdicom(self,dicom):
        return self.__mi_dicom.leerdicom(dicom)
    def validardicom(self,dicom):
        return self.__mi_edf.validardicom(dicom)

    def cargardicom (self,dicom):
        return self.__mi_dicom.cargardicom(dicom)
    def convertdicom(self, dicom):
        return self.__mi_dicom.convertdicom(dicom)
        
    def verImagen(self):
        return self.__mi_dicom.verNifti()
    
class Principal(object):
    def __init__(self): 
        self.__app = QApplication(sys.argv)
        self.__mi_vista = Ppal()
        self.__mi_edf = EDF()
        self.__mi_dicom = DICOM()
        self.__mi_controlador = Controlador(self.__mi_vista, self.__mi_edf, self.__mi_dicom)
        self.__mi_vista.asignarControlador(self.__mi_controlador)

    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())  

p=Principal()
p.main()