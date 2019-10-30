import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView, QMessageBox


class Setup(QtWidgets.QMainWindow):
    """
    Class that defines setup window in reader UI.
    """
    # Define switch window as a type of pyqtSignal, i.e., once activated the window will be switched
    switch_mainwindow = QtCore.pyqtSignal(list)
    switch_landingwindow = QtCore.pyqtSignal()

    def __init__(self, pass_val):
        super(Setup, self).__init__()

        # Load the recipe passed on from landing page
        self.recipe = pass_val[0]
        # Load the path
        self.path = pass_val[1]

        # Dimensions and style of the window
        self.setGeometry(50, 50, 600, 400)
        self.setWindowTitle('HexagonFab Experiment Setup')
        self.setWindowIcon(QtGui.QIcon('HexFab_logo.png'))
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))

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

        # Execute main window
        self.main_window()

    def main_window(self):
        # Initialize layout for widgets
        self.layout = QtWidgets.QGridLayout()
        # self.layout.setRowStretch(6, 10)
        self.recipeTable = QTableWidget()
        # Generate table with the recipe that has been passed in
        self.generate_table()

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
        self.txt_description = QtWidgets.QTextEdit('Add a description for the recipe')
        self.txt_step_name = QtWidgets.QLineEdit('Add protein1')
        self.txt_step_time = QtWidgets.QLineEdit("100")

        # #Heritage code - DO NOT DELETE - In case want to go back to create/load in this window
        # # Create new recipe file
        # self.btn_create_project = QtWidgets.QPushButton(self.pass_val)
        # self.btn_create_project.clicked.connect(self.new)
        #
        # # Load previous recipe
        # self.btn_load_project = QtWidgets.QPushButton('Load')
        # self.btn_load_project.clicked.connect(self.load)

        # Add step
        self.btn_step_add = QtWidgets.QPushButton('Add')
        self.btn_step_add.clicked.connect(self.add)

        # Reset
        self.btn_reset_recipe = QtWidgets.QPushButton('Reset')
        self.btn_reset_recipe.clicked.connect(self.PopUpReset)

        # Save
        self.btn_save = QtWidgets.QPushButton('Save')
        self.btn_save.clicked.connect(self.file_save)

        # Go to next window
        self.btn_start = QtWidgets.QPushButton("Run Recipe")
        self.btn_start.pressed.connect(self.PopUpRun)

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
        # self.layout.addWidget(self.btn_create_project, 1, 2)
        # self.layout.addWidget(self.btn_load_project, 1, 3)
        self.layout.addWidget(self.btn_step_add, 5, 4)
        self.layout.addWidget(self.btn_reset_recipe, 6, 4)
        self.layout.addWidget(self.btn_save, 8, 2)
        self.layout.addWidget(self.btn_start, 8, 3)

        self.show()

    def generate_table(self):
        print(self.recipe)
        # Create table
        self.recipeTable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.recipeTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.recipeTable.setRowCount(len(self.recipe['step_txt']))
        self.recipeTable.setColumnCount(2)
        self.recipeTable.setRowCount(5)

        self.recipeTable.setHorizontalHeaderLabels(['Step Name', 'Time'])
        # self.recipeTable.horizontalHeaderItem().setTextAlignment(QtGui.AlignHCenter)
        header = self.recipeTable.horizontalHeader()
        header.setResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setResizeMode(1, QtWidgets.QHeaderView.Stretch)

        for row in range(len(self.recipe['step_txt'])):
            self.recipeTable.setItem(row, 0, QTableWidgetItem(self.recipe['step_txt'][row]))
            self.recipeTable.setItem(row, 1, QTableWidgetItem(self.recipe['step_time'][row]))
            row += 1

        self.layout.addWidget(self.recipeTable, 6, 2, 2, 2)
        self.show()

        # table selection change
        # self.tableWidget.doubleClicked.connect(self.on_click)

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

    # # Heritage code - DO NOT DELETE - In case want to go back to create/load in this window
    # def load(self):
    #     try:
    #         file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'))[0]
    #         file = open(file_path, 'r+')  # Open with the intention to read
    #
    #         if file.mode == 'r+':  # Check if file is in 'read mode'
    #             self.recipe = {'step_txt': [], 'step_time': []}
    #
    #             for x in range(2):
    #                 next(file)
    #
    #             for line in file:
    #                 content = line.split(' : ')
    #                 self.recipe['step_txt'].append(content[0])
    #                 self.recipe['step_time'].append(content[1].rstrip())
    #
    #         self.generate_table()
    #         self.path = file_path
    #         self.BtnEnable()
    #     except:
    #         print('Load file error')

    def add(self):
        update_name = self.txt_step_name.text()
        self.recipe['step_txt'].append(update_name)

        update_time = self.txt_step_time.text()
        self.recipe['step_time'].append(update_time)
        print(self.recipe)

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

    def SwitchLanding(self):
        self.switch_landingwindow.emit()

    # # Heritage code - DO NOT DELETE - In case want to go back to create/load in this window
    # def BtnEnable(self):
    #     self.btn_step_add.setEnabled(True)
    #     self.btn_reset_recipe.setEnabled(True)
    #     self.btn_save.setEnabled(True)
    #     self.btn_start.setEnabled(True)

    # # Heritage code - DO NOT DELETE - In case want to go back to create/load in this window
    # def BtnDisable(self):
    #     pass
    #     # self.btn_step_add.setEnabled(False)
    #     # self.btn_reset_recipe.setEnabled(False)
    #     # self.btn_save.setEnabled(False)
    #     # self.btn_start.setEnabled(False)

    def PopUpReset(self):
        choice = QtWidgets.QMessageBox.question(self, 'Reset', 'Are you sure you wish to reset the recipe?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.recipe = {'step_txt': [], 'step_time': []}
            self.generate_table()
        else:
            pass

    def PopUpRun(self):
        text_message = "Set up experiment with the current recipe? \n (You will be asked to connect the sensor in the next step)"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok:
            self.file_save()
            self.SwitchMain()
        else:
            pass

