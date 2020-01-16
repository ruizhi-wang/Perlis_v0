import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QIcon, QPixmap


class landing_window(QtWidgets.QMainWindow):
    """
    Class that defines landing window, the first window to appear at program start.
    """
    # Define switch window as a type of pyqtSignal, i.e., once activated the window will be switched
    switch_setupwindow = QtCore.pyqtSignal(list)
    switch_testwindow = QtCore.pyqtSignal()

    def __init__(self):
        super(landing_window, self).__init__()

        # Create empty file path
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

        # Initialize layout for widgets
        self.layout = QtWidgets.QGridLayout()

        # HexagonFab logo
        self.logo = QtWidgets.QLabel("HexagonFab")

        # Widget initialization
        self.btn_create_project = QtWidgets.QPushButton('Set up experiment')
        self.btn_test = QtWidgets.QPushButton('Express experiment')

        # Execute main window
        self.main_window()

    def main_window(self):
        # Create layout
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.layout)

        # Populate widgets
        self.widgets()
        self.display_widgets()

    def widgets(self):
        # To display the company logo on a Windows machine, full path must be used...
        # For Mac:
        # pix_map = QPixmap('./class_landing/hexagonfab_logo_250.png')
        # For Windows:
        pix_map = QPixmap('C:/Users/Lukas/Documents/Python/Perlis_v0/class_landing/hexagonfab_logo_250.png')
        pix_map = pix_map.scaledToWidth(250, 1)
        self.logo.setPixmap(pix_map)

        # Create new recipe file
        self.btn_create_project.setStyleSheet('background-color: #4933FF; color: white; height: 25')
        self.btn_create_project.setFixedWidth(170)
        self.btn_create_project.clicked.connect(self.path_create)

        # Freestyle experiment
        self.btn_test.setFlat(True)
        self.btn_test.setStyleSheet('height: 25; margin-bottom:200; margin-top:2')
        self.btn_test.clicked.connect(self.switch_test)

    def display_widgets(self):
        # Logo
        self.layout.addWidget(self.logo, 1, 1, QtCore.Qt.AlignHCenter)

        # Buttons
        self.layout.addWidget(self.btn_create_project, 2, 1, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.btn_test, 3, 1, QtCore.Qt.AlignHCenter)

        self.show()

    def path_create(self):
        file_path = QFileDialog.getSaveFileName(self, 'Please provide path for experiment', os.getenv('HOME'))[0]
        print(file_path)

        if file_path == '':
            return

        self.path = file_path
        if self.path != '':
            self.switch_setup()
        else:
            pass

    def load_recipe(self):
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
            if self.path != '':
                self.switch_setup()
            else:
                pass
        except:
            print('Load file error')

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close', 'Are you sure you wish to exit?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def switch_setup(self):
        pass_value = [self.recipe, self.path]
        self.switch_setupwindow.emit(pass_value)

    def switch_test(self):
        self.switch_testwindow.emit()

    #-------------------------------------------------------------------------------------------------------------------
    def popup_new(self):
        text_message = "Create new or load existing project folder?"
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.addButton("Create", QMessageBox.ActionRole)
        msgBox.addButton("Load", QMessageBox.AcceptRole)
        return_value = msgBox.exec()

        if return_value == 1:
            print("1")
            self.load_recipe()
            if self.path != '':
                self.switch_setup()
            else:
                pass

        if return_value == 0:
            print("0")
            self.path_create()
            if self.path != '':
                self.switch_setup()
            else:
                pass
