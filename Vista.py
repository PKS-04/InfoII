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
        loadUi("Ppal.ui",self)
        self.setup()

