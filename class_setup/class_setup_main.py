import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QFileDialog, \
    QHeaderView, QMessageBox


class setup(QtWidgets.QMainWindow):
    """
    Class that defines setup window in reader UI.
    """
    # Define switch window1 as a type of pyqtSignal, i.e., once activated the window will be switched
    switch_mainwindow = QtCore.pyqtSignal(list)
    switch_landingwindow = QtCore.pyqtSignal()

    def __init__(self, pass_val):
        super(setup, self).__init__()

        # Load the recipe passed on from landing page
        self.recipe = pass_val[0]
        # Load the path
        self.path = pass_val[1]

        # Dimensions and style of the window
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('HexagonFab Experiment Setup')
        self.setWindowIcon(QtGui.QIcon('HexFab_logo.png'))
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))

        # Create tool bar
        self.toolBar = self.addToolBar('Create')

        # Tool Bar - Define Actions
        self.return_home = QtWidgets.QAction('< Back', self)
        self.return_home.triggered.connect(self.SwitchLanding)
        self.toolBar.addAction(self.return_home)

        # Text editor deactivated until important rationale for it is found :)
        # self.open_editor = QtWidgets.QAction('Text editor', self)
        # self.open_editor.triggered.connect(self.editor)
        # self.toolBar.addAction(self.open_editor)

        self.closeWindow = QtWidgets.QAction('Close', self)
        self.closeWindow.setShortcut('Ctrl+W')
        self.closeWindow.setStatusTip('Quit app')
        self.closeWindow.triggered.connect(self.close_app)
        self.toolBar.addAction(self.closeWindow)

        # Initialize widgets
        self.layout = QtWidgets.QGridLayout()
        # self.layout.setRowStretch(6, 10)
        self.recipe_table = QTableWidget()
        self.header_label = QtGui.QLabel('HexagonFab')

        self.lbl_load = QtWidgets.QLabel('Load steps from existing recipe')
        self.lbl_description = QtWidgets.QLabel('Set up your protocol')
        self.lbl_recipe = QtWidgets.QLabel('Protocol')
        self.lbl_step_name = QtWidgets.QLabel('Input step name')
        self.lbl_step_time = QtWidgets.QLabel('Step duration')

        self.protocol_description = 'Add protocol description...'

        self.txt_description = QtWidgets.QTextEdit(self.protocol_description)
        self.txt_step_name = QtWidgets.QLineEdit('Add step name...')
        self.txt_step_time = QtWidgets.QLineEdit("0")

        self.btn_load = QtWidgets.QPushButton('Load')
        self.btn_step_add = QtWidgets.QPushButton('Add')
        self.btn_reset_recipe = QtWidgets.QPushButton('Reset')
        self.btn_save = QtWidgets.QPushButton('Save')
        self.btn_start = QtWidgets.QPushButton("Continue >")

        # Execute main window
        self.main_window()

    def main_window(self):
        # Generate table with recipe
        self.generate_recipe_table()

        # Create layout
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.layout)
        self.generate_recipe_table()

        # Populate widgets
        self.widgets()
        self.display_widgets()

    def widgets(self):
        # To display the company logo on a Windows machine, full path must be used...
        # For Mac:
        # pix_map = QPixmap('./class_landing/hexagonfab_logo_250.png')
        # For Windows:
        pix_map = QPixmap('C:/Users/Lukas/Documents/Python/Perlis_v0/class_landing/hexagonfab_logo_250.png')
        pix_map = pix_map.scaledToWidth(100, 1)
        self.header_label.setPixmap(pix_map)

        self.lbl_load.setStyleSheet("font-weight:bold; font-size:25")
        self.lbl_description.setStyleSheet("font-weight:bold; font-size:25")

        self.lbl_recipe.setStyleSheet("font-weight:bold")
        self.lbl_step_name.setStyleSheet("font-weight:bold")
        self.lbl_step_time.setStyleSheet("font-weight:bold")

        self.txt_description.setFixedHeight(50)
        self.txt_step_name.setStyleSheet("alignment:top")

        # #Heritage code - DO NOT DELETE - In case want to go back to create/load in this window
        # # Create new protocol file
        # self.btn_create_project = QtWidgets.QPushButton(self.pass_val)
        # self.btn_create_project.clicked.connect(self.new)
        #
        # # Load previous protocol
        # self.btn_load_project = QtWidgets.QPushButton('Load')
        # self.btn_load_project.clicked.connect(self.load)

        # Load existing recipe file
        self.btn_load.setStyleSheet("height: 25; margin-top:15")
        self.btn_load.setFixedWidth(150)
        self.btn_load.clicked.connect(self.load_recipe)

        # Add step
        # self.btn_step_add.setFixedWidth(40)
        self.btn_step_add.clicked.connect(self.add)

        # Reset
        self.btn_reset_recipe.setStyleSheet("background-color: #6A3A3A; height: 25;margin-top:15;")
        self.btn_reset_recipe.setFixedWidth(100)
        self.btn_reset_recipe.clicked.connect(self.PopUpReset)

        # Save
        # self.btn_save.setStyleSheet("height: 25;margin-top:15;")
        # self.btn_save.setFixedWidth(150)
        # self.btn_save.clicked.connect(self.file_save)

        # Go to next window
        self.btn_start.setStyleSheet("background-color: #4933FF; color: white; height: 25;margin-top:15; ")
        self.btn_start.setFixedWidth(100)
        self.btn_start.pressed.connect(self.PopUpRun)

    # Assign widget locations based on grid layout
    def display_widgets(self):
        # HexagonFab label
        self.layout.addWidget(self.header_label, 1, 2, 1, 1)

        # Load button and description
        # self.layout.addWidget(self.lbl_load, 2, 2, 1, 1)
        # self.layout.addWidget(self.btn_load, 4, 2, 1, 1)

        # Description
        self.layout.addWidget(self.lbl_description, 2, 2, 1, 1)
        self.layout.addWidget(self.txt_description, 4, 2, 1, 4)

        # Protocol build
        self.layout.addWidget(self.lbl_recipe, 5, 2)

        self.layout.addWidget(self.lbl_step_name, 13, 2, 1, 1)
        self.layout.addWidget(self.txt_step_name, 14, 2, 1, 1)

        self.layout.addWidget(self.lbl_step_time, 13, 3, 1, 2)
        self.layout.addWidget(self.txt_step_time, 14, 3, 1, 2)

        # Buttons
        # self.layout.addWidget(self.btn_create_project, 1, 2)
        # self.layout.addWidget(self.btn_load_project, 1, 3)
        # self.layout.addWidget(self.btn_step_add, 14, 5, 1, 1, QtCore.Qt.AlignRight)
        self.layout.addWidget(self.btn_step_add, 14, 5, 1, 1, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.btn_reset_recipe, 16, 2, 2, 1)
        self.layout.addWidget(self.btn_load, 16, 2, 2, 4, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.btn_start, 16, 5, 2, 1, QtCore.Qt.AlignRight)

        # Recipe table
        self.layout.addWidget(self.recipe_table, 6, 2, 4, 4)

        self.show()

    # Generate and populate table from user data
    def generate_recipe_table(self):
        self.recipe_table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.recipe_table.setRowCount(len(self.recipe['step_txt']))
        self.recipe_table.setColumnCount(2)

        # self.recipe_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.recipe_table.setHorizontalHeaderLabels(['Step Name', 'Duration'])
        # self.recipe_table.horizontalHeaderItem().setTextAlignment(QtGui.AlignHCenter)
        header = self.recipe_table.horizontalHeader()
        header.setResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Populate table with recipe data
        for row in range(len(self.recipe['step_txt'])):
            self.recipe_table.setItem(row, 0, QTableWidgetItem(self.recipe['step_txt'][row]))
            self.recipe_table.setItem(row, 1, QTableWidgetItem(self.recipe['step_time'][row]))
            row += 1

        self.recipe_table.setFixedHeight(400)
        self.recipe_table.resizeRowsToContents()

        # Update recipe file from direct user table input
        self.recipe_table.itemChanged.connect(self.user_update)

        self.show()

    # Load recipe from earlier project
    def load_recipe(self):
        try:
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'))[0]
            file = open(file_path, 'r+')  # Open with the intention to read

            if file.mode == 'r+':  # Check if file is in 'read mode'
                self.recipe = {'step_txt': [], 'step_time': []}
                # self.protocol_description = file.readline()
                # print(self.protocol_description)

                for x in range(2):
                    next(file)

                for line in file:
                    content = line.split(' : ')
                    self.recipe['step_txt'].append(content[0])
                    self.recipe['step_time'].append(content[1].rstrip())

            self.generate_recipe_table()
        except:
            print('Load file error')

    # Update protocol based on direct changes to table
    def user_update(self, item):
        if item.column() == 0:
            self.recipe['step_txt'][item.row()] = item.text()
        elif item.column() == 1:
            self.recipe['step_time'][item.row()] = item.text()
        else:
            pass

    # Save data to file
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

    # Append recipe dictionary with user data; regenerate table
    def add(self):
        update_name = self.txt_step_name.text()
        self.recipe['step_txt'].append(update_name)

        update_time = self.txt_step_time.text()
        self.recipe['step_time'].append(update_time)

        self.generate_recipe_table()

    # Open a text editor in the main window
    def editor(self):
        self.textEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.textEdit)

    # Exit main window
    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close', 'Are you sure you wish to exit?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def SwitchMain(self):
        pass_value = [self.recipe, self.path]
        self.switch_mainwindow.emit(pass_value)

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
        choice = QtWidgets.QMessageBox.question(self, 'Reset', 'Are you sure you wish to reset the protocol?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.txt_description = QtWidgets.QTextEdit('Add protocol description...')
            self.recipe = {'step_txt': [], 'step_time': []}
            self.generate_recipe_table()
        else:
            pass

    def PopUpRun(self):
        self.file_save()
        text_message = "Ready to set up experiment?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            self.file_save()
            self.SwitchMain()
        else:
            pass
