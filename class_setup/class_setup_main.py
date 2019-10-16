import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout

class Setup(QtWidgets.QMainWindow):

    # Define switch window as a type of pyqtSignal - i.e. once activated the window will be switched
    switch_window = QtCore.pyqtSignal(list)

    def __init__(self):
        super(Setup, self).__init__()

        # Dimensions and style of the window
        self.setGeometry(50, 50, 600, 300)
        self.setWindowTitle('HexagonFab Experiment Setup')
        self.setWindowIcon(QtGui.QIcon('HexFab_logo.png'))
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))

        # File open, file save, and close menu actions
        fileOpen = QtWidgets.QAction('&Open', self)
        fileOpen.setShortcut('Ctrl+O')
        fileOpen.setStatusTip('Open file')
        fileOpen.triggered.connect(self.file_open)

        fileSave = QtWidgets.QAction('&Save', self)
        fileSave.setShortcut('Ctrl+S')
        fileSave.setStatusTip('Save file')
        fileSave.triggered.connect(self.file_save)

        closeAction = QtWidgets.QAction('&Close', self)
        closeAction.setShortcut('Ctrl+W')
        closeAction.setStatusTip('Quit app')
        closeAction.triggered.connect(self.close_app)

        self.statusBar()

        # Generate main menu items
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(fileOpen)
        fileMenu.addAction(fileSave)
        fileMenu.addAction(closeAction)

        optionsMenu = mainMenu.addMenu('&Options')
        optionsMenu.addAction(closeAction)

        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(closeAction)

        # Populate tool bar
        returnHome = QtWidgets.QAction('Home', self)
        returnHome.triggered.connect(self.main_window)

        openEditor = QtWidgets.QAction('Text editor', self)
        openEditor.triggered.connect(self.editor)

        self.toolBar = self.addToolBar('Create')
        self.toolBar.addAction(returnHome)
        self.toolBar.addAction(openEditor)

        # Setup data
        self.recipe = {'step_txt': ["base"], 'step_time': ["100"]}

        # Execute main window
        self.main_window()

        # Dummy path
        self.path = ""

    def main_window(self):
        # Initialize
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.layout = QtWidgets.QGridLayout()
        self.centralWidget().setLayout(self.layout)
        self.generate_table()
        # Populate widgets
        self.widgets()
        self.display_widgets()

    def widgets(self):
        # UI labels
        self.lbl_exp_title = QtWidgets.QLabel('Experiment Title:')
        self.lbl_step_name = QtWidgets.QLabel('Step Name:')
        self.lbl_step_time = QtWidgets.QLabel('Step Time [s]:')

        # User text input
        self.txt_exp_title = QtWidgets.QLineEdit()
        self.txt_step_name = QtWidgets.QLineEdit()
        self.txt_step_time = QtWidgets.QLineEdit("100")

        # Upload step information
        self.btn_step_upload = QtWidgets.QPushButton('Add')
        self.btn_step_upload.clicked.connect(self.Upload)

        # Go to next window
        self.btn_start = QtWidgets.QPushButton("Start Experiment")
        self.btn_start.pressed.connect(self.switch)

        # Reset button
        self.btn_reset_recipe = QtWidgets.QPushButton('Reset')
        self.btn_reset_recipe.clicked.connect(self.reset)

    def display_widgets(self):
        # Assign widget locations based on grid layout
        self.layout.addWidget(self.lbl_exp_title, 2, 1)
        self.layout.addWidget(self.lbl_step_name, 3, 1)
        self.layout.addWidget(self.lbl_step_time, 4, 1)

        self.layout.addWidget(self.txt_exp_title, 2, 2)
        self.layout.addWidget(self.txt_step_name, 3, 2)
        self.layout.addWidget(self.txt_step_time, 4, 2)

        self.layout.addWidget(self.btn_start, 2, 3)
        self.layout.addWidget(self.btn_step_upload, 4, 3)
        self.layout.addWidget(self.btn_reset_recipe, 5, 3)

        self.show()

    def generate_table(self):
        # Create table
        self.recipeTable = QTableWidget()
        self.recipeTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.recipeTable.setRowCount(len(self.recipe['step_txt']))
        self.recipeTable.setColumnCount(2)
        print(self.recipe)

        row = 0
        for i in range(0, len(self.recipe['step_txt'])):
            self.recipeTable.setItem(row, 0, QTableWidgetItem(self.recipe['step_txt'][i]))
            self.recipeTable.setItem(row, 1, QTableWidgetItem(self.recipe['step_time'][i]))
            row+=1

        self.layout.addWidget(self.recipeTable, 5, 2)

        self.show()

    ##        table selection change
    ##        self.tableWidget.doubleClicked.connect(self.on_click)

    def reset(self):
        self.recipe = {'step_txt':[], 'step_time':[]}
        self.generate_table()

    def Upload(self):
        update_name = self.txt_step_name.text()
        self.recipe['step_txt'].append(update_name)

        update_time = self.txt_step_time.text()
        self.recipe['step_time'].append(update_time)

        self.generate_table()

    def file_open(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
        file = open(name, 'r')  # Open with the intention to read

        self.editor()

        with file:
            text = file.read()
            self.textEdit.setText(text)

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file')[0]
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

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

        # self.experiment_step = {"time": ["10", "20", "30"], "steps": ["baseline", "avidin", "baseline"]}

    def switch(self):
        pass_val = [self.recipe, self.path]
        self.switch_window.emit(pass_val)