import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QFileDialog


class LandingWindow(QtWidgets.QMainWindow):
    """
    Class that defines setup window in reader UI.
    """
    # Define switch window as a type of pyqtSignal, i.e., once activated the window will be switched
    switch_setupwindow = QtCore.pyqtSignal()
    switch_testwindow = QtCore.pyqtSignal()

    def __init__(self):
        super(LandingWindow, self).__init__()

        # Dimensions and style of the window
        self.setGeometry(50, 50, 100, 100)
        self.setWindowTitle('HexagonFab Landing')
        self.setWindowIcon(QtGui.QIcon('HexagonFab_RGB.jpg'))
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))

        # Actions for file open, file save, and close menu actions
        file_open = QtWidgets.QAction('&Open', self)
        file_open.setShortcut('Ctrl+O')
        file_open.setStatusTip('Open file')

        file_save = QtWidgets.QAction('&Save', self)
        file_save.setShortcut('Ctrl+S')
        file_save.setStatusTip('Save file')

        close_action = QtWidgets.QAction('&Close', self)
        close_action.setShortcut('Ctrl+W')
        close_action.setStatusTip('Quit app')
        close_action.triggered.connect(self.close_app)

        self.statusBar()

        # Generate main menu items
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(file_open)
        file_menu.addAction(file_save)
        file_menu.addAction(close_action)

        options_menu = main_menu.addMenu('&Options')
        options_menu.addAction(close_action)

        help_menu = main_menu.addMenu('&Help')
        help_menu.addAction(close_action)

        # Create tool bar
        self.toolBar = self.addToolBar('Create')

        # Tool Bar - Define Actions
        self.return_home = QtWidgets.QAction('Home', self)
        self.return_home.triggered.connect(self.main_window)
        self.toolBar.addAction(self.return_home)

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

        # Create new recipe file
        self.btn_create_project = QtWidgets.QPushButton('Create new experiment')
        self.btn_create_project.setStyleSheet("background-color: blue")
        self.btn_create_project.clicked.connect(self.SwitchSetup)

        # Freestyle experiment
        self.btn_test = QtWidgets.QPushButton('Test Experiment')
        self.btn_test.clicked.connect(self.SwitchTest)

    def display_widgets(self):
        # Buttons
        self.layout.addWidget(self.btn_create_project, 1, 1)
        self.layout.addWidget(self.btn_test, 2, 1)

        self.show()

    def new(self):
        description = "Empty"

        file_path = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))[0]

        filename_recipe=file_path+"_recipe.txt"

        with open(filename_recipe, "w") as file:
            file.write(description + '\n')

        if file_path == '':
            return
        else:
            self.BtnEnable()

        self.path = file_path

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close', 'Are you sure you wish to exit?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def SwitchSetup(self):
        self.switch_setupwindow.emit()

    def SwitchTest(self):
        self.switch_testwindow.emit()