import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
import pyqtgraph as pg
import numpy as np
import serial
import time
import os

class PopUp(QtWidgets.QMainWindow):

    def __init__(self, message_value='', pass_value=[]):
        super(PopUp, self).__init__()

        self.message = message_value
        self.pass_value = pass_value



    def PopUp_Check(self):
        print("call")
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("text")

        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # msgBox.QMessageBox
        print(self.pass_value)
        # msgBox.buttonClicked.connect(msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')