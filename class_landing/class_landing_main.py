import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap

class LandingWindow(QtWidgets.QMainWindow):
    """
    Class that defines setup window in reader UI.
    """
    # Define switch window as a type of pyqtSignal, i.e., once activated the window will be switched
    switch_setupwindow = QtCore.pyqtSignal(list)
    switch_testwindow = QtCore.pyqtSignal()


    def __init__(self):
        super(LandingWindow, self).__init__()

        self.path = ''
        self.recipe = {'step_txt': [], 'step_time': []}

        # Dimensions and style of the window
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('HexagonFab Analysis App')
        self.setWindowIcon(QtGui.QIcon('HexagonFab_RGB.jpg'))
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))

        # Create tool bar
        self.toolBar = self.addToolBar('Create')

        # Tool Bar - Define Actions
        # self.return_home = QtWidgets.QAction('Home', self)
        # self.return_home.triggered.connect(self.main_window)
        # self.toolBar.addAction(self.return_home)

        self.closeWindow = QtWidgets.QAction('Close', self)
        self.closeWindow.setShortcut('Ctrl+W')
        self.closeWindow.setStatusTip('Quit app')
        self.closeWindow.triggered.connect(self.close_app)
        self.toolBar.addAction(self.closeWindow)

        # Create empty file path
        # self.path = 'path_file'
        self.path = ''

        # Execute main window
        self.main_window()

    def main_window(self):
        # Initialize layout for widgets
        self.layout = QtWidgets.QGridLayout()
        self.recipeTable = QTableWidget()

        # Create layout
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.layout)

        # Populate widgets
        self.widgets()
        self.display_widgets()

    def widgets(self):

        # Show HexagonFab logo
        self.logo = QtWidgets.QLabel("HexagonFab")
        pixmap = QPixmap('./class_landing/hexagonfab_logo_250.png')
        pixmap = pixmap.scaledToWidth(250, 1)
        self.logo.setPixmap(pixmap)

        # Create new recipe file
        self.btn_create_project = QtWidgets.QPushButton('Set up experiment')
        self.btn_create_project.setStyleSheet("background-color: #4933FF; \
                                              color: white; \
                                              height: 25; \
                                              ")
        self.btn_create_project.setFixedWidth(170)
        self.btn_create_project.clicked.connect(self.PopUpNew)

        # Freestyle experiment
        self.btn_test = QtWidgets.QPushButton('Express Experiment')
        self.btn_test.setFlat(True)
        self.btn_test.setStyleSheet("height: 25;margin-bottom:200;margin-top:2;")
        self.btn_test.clicked.connect(self.SwitchTest)

    def display_widgets(self):

        # Logo
        self.layout.addWidget(self.logo, 1,1,QtCore.Qt.AlignHCenter)

        # Buttons
        self.layout.addWidget(self.btn_create_project, 2, 1, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.btn_test, 3, 1, QtCore.Qt.AlignHCenter)

        self.show()



    def PathCreate(self):
        description = "Empty"

        file_path = QFileDialog.getSaveFileName(self, 'Please provide path for experiment', os.getenv('HOME'))[0]

        if file_path == '':
            return

        self.path = file_path

    def LoadRecipe(self):
        try:
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'))[0]
            file = open(file_path, 'r+')  # Open with the intention to read

            if file.mode == 'r+':  # Check if file is in 'read mode'
                self.recipe = {'step_txt': [], 'step_time': []}

                for x in range(2):
                    next(file)

                for line in file:
                    content = line.split(' : ')
                    self.recipe['step_txt'].append(content[0])
                    self.recipe['step_time'].append(content[1].rstrip())

            self.path = file_path
        except:
            print('Load file error')

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close', 'Are you sure you wish to exit?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def SwitchSetup(self):
        pass_val=[self.recipe, self.path]
        self.switch_setupwindow.emit(pass_val)

    def SwitchTest(self):
        self.switch_testwindow.emit()

    #-------------------------------------------------------------------------------------------------------------------
    def PopUpNew(self):
        text_message = "Create new or load existing protocol?"
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.addButton("Create", QMessageBox.ActionRole)
        msgBox.addButton("Load", QMessageBox.AcceptRole)
        returnValue = msgBox.exec()


        if returnValue == 1:
            print("1")
            self.LoadRecipe()
            if self.path != '':
                self.SwitchSetup()
            else:
                pass

        if returnValue == 0:
            print("0")
            self.PathCreate()
            if self.path != '':
                self.SwitchSetup()
            else:
                pass