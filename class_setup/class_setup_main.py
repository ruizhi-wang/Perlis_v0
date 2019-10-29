import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QFileDialog


class Setup(QtWidgets.QMainWindow):
    """
    Class that defines setup window in reader UI.
    """
    # Define switch window as a type of pyqtSignal, i.e., once activated the window will be switched
    switch_mainwindow = QtCore.pyqtSignal(list)
    switch_testwindow = QtCore.pyqtSignal()
    switch_landingwindow = QtCore.pyqtSignal()

    def __init__(self):
        super(Setup, self).__init__()

        # Dimensions and style of the window
        self.setGeometry(50, 50, 600, 300)
        self.setWindowTitle('HexagonFab Experiment Setup')
        self.setWindowIcon(QtGui.QIcon('HexFab_logo.png'))
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))

        # Actions for file open, file save, and close menu actions
        file_open = QtWidgets.QAction('&Open', self)
        file_open.setShortcut('Ctrl+O')
        file_open.setStatusTip('Open file')
        file_open.triggered.connect(self.load)

        file_save = QtWidgets.QAction('&Save', self)
        file_save.setShortcut('Ctrl+S')
        file_save.setStatusTip('Save file')
        file_save.triggered.connect(self.file_save)

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
        self.return_home.triggered.connect(self.SwitchLanding)
        self.toolBar.addAction(self.return_home)

        self.open_editor = QtWidgets.QAction('Text editor', self)
        self.open_editor.triggered.connect(self.editor)
        self.toolBar.addAction(self.open_editor)

        self.closeWindow = QtWidgets.QAction('Close', self)
        self.closeWindow.setShortcut('Ctrl+W')
        self.closeWindow.setStatusTip('Quit app')
        self.closeWindow.triggered.connect(self.close_app)
        self.toolBar.addAction(self.closeWindow)




        # Setup data
        # self.recipe = {'step_txt': ["base", "base"], 'step_time': ["100", "10"]}
        self.recipe = {'step_txt': [], 'step_time': []}

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
        self.generate_table()

        # Populate widgets
        self.widgets()
        self.display_widgets()

    def widgets(self):
        # UI labels
        self.lbl_description = QtWidgets.QLabel('Description:')
        self.lbl_step_name = QtWidgets.QLabel('Step Name:')
        self.lbl_step_time = QtWidgets.QLabel('Step Time [s]:')
        self.lbl_recipe = QtWidgets.QLabel('Recipe:')

        # User text input
        self.txt_description = QtWidgets.QTextEdit('Test protein affinity')
        self.txt_step_name = QtWidgets.QLineEdit('Add protein1')
        self.txt_step_time = QtWidgets.QLineEdit("100")

        # Create new recipe file
        self.btn_create_project = QtWidgets.QPushButton('New')
        self.btn_create_project.clicked.connect(self.new)

        # Load previous recipe
        self.btn_load_project = QtWidgets.QPushButton('Load')
        self.btn_load_project.clicked.connect(self.load)

        # Freestyle experiment
        self.btn_test = QtWidgets.QPushButton('Test Experiment')
        self.btn_test.clicked.connect(self.SwitchTest)

        # Add step
        self.btn_step_add = QtWidgets.QPushButton('Add')
        self.btn_step_add.clicked.connect(self.add)

        # Reset
        self.btn_reset_recipe = QtWidgets.QPushButton('Reset')
        self.btn_reset_recipe.clicked.connect(self.reset)

        # Save
        self.btn_save = QtWidgets.QPushButton('Save')
        self.btn_save.clicked.connect(self.file_save)

        # Go to next window
        self.btn_start = QtWidgets.QPushButton("Start Experiment")
        self.btn_start.pressed.connect(self.SwitchMain)

    def display_widgets(self):
        # Assign widget locations based on grid layout

        # Text labels
        self.layout.addWidget(self.lbl_description, 2, 1)
        self.layout.addWidget(self.lbl_step_name, 4, 2)
        self.layout.addWidget(self.lbl_step_time, 4, 3)
        self.layout.addWidget(self.lbl_recipe, 6, 1)

        # Line edits
        self.layout.addWidget(self.txt_description, 2, 2, 2, 2)
        self.layout.addWidget(self.txt_step_name, 5, 2)
        self.layout.addWidget(self.txt_step_time, 5, 3)

        # Buttons
        self.layout.addWidget(self.btn_create_project, 1, 2)
        self.layout.addWidget(self.btn_load_project, 1, 3)
        self.layout.addWidget(self.btn_test, 1, 4)
        self.layout.addWidget(self.btn_step_add, 5, 4)
        self.layout.addWidget(self.btn_reset_recipe, 6, 4)
        self.layout.addWidget(self.btn_save, 8, 2)
        self.layout.addWidget(self.btn_start, 8, 3)

        self.BtnDisable()

        self.show()

    def generate_table(self):
        # Create table
        self.recipeTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.recipeTable.setRowCount(len(self.recipe['step_txt']))
        self.recipeTable.setColumnCount(2)

        for row in range(len(self.recipe['step_txt'])):
            self.recipeTable.setItem(row, 0, QTableWidgetItem(self.recipe['step_txt'][row]))
            self.recipeTable.setItem(row, 1, QTableWidgetItem(self.recipe['step_time'][row]))
            row += 1

        self.layout.addWidget(self.recipeTable, 6, 2, 2, 2)
        self.show()

        # table selection change
        # self.tableWidget.doubleClicked.connect(self.on_click)

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

    def file_save(self):
        try:
            file_path = self.path
            description = self.txt_description.toPlainText()
            file = open(file_path+"_recipe.txt", 'w+')

            file.write(description + '\n\n')

            for i in range(len(self.recipe['step_txt'])):
                file.write(self.recipe['step_txt'][i] + ' : ' + self.recipe['step_time'][i] + '\n')
        except:
            print('File save error')


    def load(self):
        try:
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'TXT (*.txt)')[0]
            file = open(file_path, 'r')  # Open with the intention to read

            if file.mode == 'r':  # Check if file is in 'read mode'
                self.recipe = {'step_txt': [], 'step_time': []}

                for x in range(2):
                    next(file)

                for line in file:
                    content = line.split(' : ')
                    self.recipe['step_txt'].append(content[0])
                    self.recipe['step_time'].append(content[1].rstrip())

            self.generate_table()
            self.path = file_path
            self.BtnEnable()
        except:
            print('Load file error')

    def add(self):
        update_name = self.txt_step_name.text()
        self.recipe['step_txt'].append(update_name)

        update_time = self.txt_step_time.text()
        self.recipe['step_time'].append(update_time)
        print(self.recipe)

        self.generate_table()

    def reset(self):
        self.recipe = {'step_txt': [], 'step_time': []}
        self.generate_table()

    def editor(self):
        self.textEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.textEdit)

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close', 'Are you sure you wish to exit?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def SwitchMain(self):
        pass_val = [self.recipe, self.path]
        self.switch_mainwindow.emit(pass_val)

    def SwitchTest(self):
        self.switch_testwindow.emit()

    def SwitchLanding(self):
        self.switch_landingwindow.emit()

    def BtnEnable(self):
        self.btn_step_add.setEnabled(True)
        self.btn_reset_recipe.setEnabled(True)
        self.btn_save.setEnabled(True)
        self.btn_start.setEnabled(True)

    def BtnDisable(self):
        self.btn_step_add.setEnabled(False)
        self.btn_reset_recipe.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_start.setEnabled(False)