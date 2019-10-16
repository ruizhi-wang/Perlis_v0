import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
import pyqtgraph as pg
import numpy as np
import serial
import time
from datetime import date

# Window setting up experiment
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
        self.path = "/Users/ruizhiwang/Desktop"

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

# Window for monitoring and running the experiment
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, pass_value):
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 600, 300)

        self.setWindowTitle('HexagonFab Run Experiment')
        self.setWindowIcon(QtGui.QIcon('HexFab_logo.png'))

        # Initialize the time counter
        self.counter = 0
        # Initialize step counter
        self.step_tracker = 0
        self.experiment_steps = pass_value[0]
        self.path = pass_value[1]

        # Initialize communication with Arduino
        self.go_state = False  # Create class variables (i.e. go_state)
        self.save_timer = 0
        try:
            # self.ard = serial.Serial(
            #    port='COM1',
            #    baudrate=500000,
            #    timeout=2
            # )
            time.sleep(2)  # Pause execution for 2 seconds
            self.go_state = False
        except:
            self.go_state = False
        # Setting up the data sets for saving and displaying
        self.data = {
            'data1': [],
            'data2': [],
            'data3': [],
            'data4': [],
            'notes': [[0.0, 0.0, 'start_program']],
        }
        self.time_start_true = time.time()  # Number of seconds since time epoch
        self.display_no = 500  # Initial amount of data points displayed

        # Timer to data collect
        self.timer = QtCore.QTimer()                    # Create QTimer instance
        self.timer.timeout.connect(self.UpdateData)     # Update data at constant time intervals
        self.timer.timeout.connect(self.UpdateGraph)    # Update UI graph at constant time intervals

        # Populate tool bar
        self.toolBar = self.addToolBar('Create')
        returnHome = QtWidgets.QAction('Home', self)
        openEditor = QtWidgets.QAction('Text editor', self)
        self.toolBar.addAction(returnHome)
        self.toolBar.addAction(openEditor)

        # Main UI
        self.main_window()

    def main_window(self):
        # Initialize
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.layout = QtWidgets.QGridLayout()
        self.centralWidget().setLayout(self.layout)

        # Populate widgets
        self.widgets()
        self.display_widgets()

        # Save a Dummy file
        self.Save()

    def widgets(self):
        
        # Code Olli --------------------------------------------
        # Start and stop button and connection
        self.btn_start = QtGui.QPushButton('start')  # Create instance of QPushButton
        self.btn_start.clicked.connect(self.StartRecording)  # Call StartRecording function when start button pressed
        self.btn_stop = QtGui.QPushButton('stop')
        self.btn_stop.clicked.connect(self.StopRecording)  # Call StopRecording function at button press
        self.btn_reset = QtGui.QPushButton('Reset')
        self.btn_reset.clicked.connect(self.Reset)  # Call Reset function at button press

        # Note text and connection
        self.txt_note = QtGui.QLineEdit('note')  # Create instance of QLineEdit
        self.btn_note = QtGui.QPushButton('add note')  # Create instance of QPushButton
        self.btn_note.clicked.connect(self.AddNote)  # Call AddNote function at button press

        # Save, file and text widgets and connections
        # self.txt_file = QtGui.QLineEdit('file_name')  # Create instance of QLineEdit
        # self.btn_save = QtGui.QPushButton('save')  # Create instance of QPushButton
        # self.btn_save.clicked.connect(self.Save)  # Call Save function at button press
        self.btn_file = QtGui.QPushButton('file...')  # Create instance of QPushButton
        self.btn_file.clicked.connect(self.ChooseFile)  # Call ChooseFile function at button press

        # What - data widgets
        self.data_select1 = QtGui.QCheckBox('Sensor1')  # Create instance of QCheckBox
        self.data_select2 = QtGui.QCheckBox('Sensor2')  # Create instance of QCheckBox
        self.data_select3 = QtGui.QCheckBox('Averages')  # Create instance of QCheckBox

        # No-points box
        self.points_label = QtGui.QLabel('No data points : ')  # Create instance of QLabel
        self.txt_points = QtGui.QLineEdit('500')  # Create instance of QLineEdit

        # Comport select
        self.com_label = QtGui.QLabel('Com Port : ')  # Create instance of QLabel
        self.com_select = QtGui.QComboBox()  # Create instance of QComboBox
        for port in ['COM' + str(x) for x in range(12)]:
            self.com_select.addItem(port)  # Call Qt function addItem on self.com_select
        self.com_select.currentIndexChanged.connect(self.SetPort)  # Call SetPort function to select com port

        # Plot widgets and lines
        self.plot = pg.PlotWidget()
        self.l1 = self.plot.plot(pen=pg.mkPen('r', width=3))
        self.l2 = self.plot.plot(pen=pg.mkPen('b', width=3))
        self.l3 = self.plot.plot(pen=pg.mkPen('w', width=3))
        self.l4 = self.plot.plot(pen=pg.mkPen('r', width=3, style=QtCore.Qt.DashLine))
        self.l5 = self.plot.plot(pen=pg.mkPen('b', width=3, style=QtCore.Qt.DashLine))
        self.l6 = self.plot.plot(pen=pg.mkPen('w', width=3, style=QtCore.Qt.DashLine))

        #--------------------------------------------
        self.time_counter = QtWidgets.QLabel("Press NEXT to start experiment")
        self.duration_counter = QtWidgets.QLabel()
        self.step_counter = QtWidgets.QLabel()
        self.duration_next = QtWidgets.QLabel()
        self.step_next = QtWidgets.QLabel()

        self.button_experiment = QtWidgets.QPushButton("next")
        self.button_experiment.pressed.connect(lambda x=self.experiment_steps: self.step_experiment(x))

    def display_widgets(self):
        # Code from Olli --------------------------------------------
        # Build all widgets and set locations
        self.layout.addWidget(self.btn_start, 1, 3)
        self.layout.addWidget(self.btn_stop, 0, 3)
        self.layout.addWidget(self.btn_reset, 2, 3)

        self.layout.addWidget(self.points_label, 0, 0)
        self.layout.addWidget(self.txt_points, 0, 1)

        self.layout.addWidget(self.data_select1, 0, 2)
        self.layout.addWidget(self.data_select2, 1, 2)
        self.layout.addWidget(self.data_select3, 2, 2)

        self.layout.addWidget(self.com_select, 1, 1)
        self.layout.addWidget(self.com_label, 1, 0)

        # self.layout.addWidget(self.btn_note, 1, 1)
        self.layout.addWidget(self.btn_note, 2, 1)
        self.layout.addWidget(self.txt_note, 2, 0)
        # layout.addWidget(listw, 3, 0)
        self.layout.addWidget(self.plot, 3, 0, 1, 4)  # Add plot (int row, int column, int rowSpan, int columnSpan)

        self.layout.addWidget(self.btn_file, 4, 2)
        # self.layout.addWidget(self.txt_file, 4, 0, 1, 2)
        # self.layout.addWidget(self.btn_save, 4, 3)
        #--------------------------------------------
        
        # Assign widget locations based on grid layout
        self.layout.addWidget(self.time_counter, 5, 1)
        self.layout.addWidget(self.duration_counter, 5, 2)
        self.layout.addWidget(self.step_counter, 6, 2)
        self.layout.addWidget(self.duration_next, 6, 1)
        self.layout.addWidget(self.step_next, 7, 2)
        self.layout.addWidget(self.button_experiment, 7, 1)

        self.show()

    def timer_counter(self):
        # Timer to keep track of time passed for each period
        self.timer_experiment = QtCore.QTimer()
        self.timer_experiment.setInterval(1000)
        self.timer_experiment.timeout.connect(self.recurring_timer)
        self.timer_experiment.start()

    def recurring_timer(self):
        self.counter -= 1
        self.time_counter.setText("Time remaining: %d" % self.counter)

    def step_experiment(self, experiment_steps):
        a=len(experiment_steps["step_time"])

        if self.step_tracker < a:
            self.timer_counter()
            # Get index of current step
            self.counter = int(experiment_steps["step_time"][self.step_tracker])
        else:
            self.timer_counter()
            self.timer_experiment.stop()
            self.time_counter.setText("Time remaining: Experiment over")

        if self.step_tracker < a:
            # Display information about current step
            self.step_counter.setText("Name of current step: " + experiment_steps["step_txt"][self.step_tracker])
            self.duration_counter.setText("Duration of current step: " + experiment_steps["step_time"][self.step_tracker])
        else:
            self.step_counter.setText("End of Experiment")
            self.duration_counter.setText("End of Experiment")

        if self.step_tracker+1<a:
            # Display information about next step
            self.step_next.setText("Name of next step: " + experiment_steps["step_txt"][self.step_tracker+1])
            self.duration_next.setText("Duration of next step: " + experiment_steps["step_time"][self.step_tracker+1])
        else:
            self.step_next.setText("End of Experiment")
            self.duration_next.setText("End of Experiment")

        self.step_tracker += 1
    # Communicate with Arduino to receive data
    def UpdateData(self):
        time_true = time.time() - self.time_start_true
        time_sincestart = time.time() - self.time_start
        try:
            self.ard.write(b'1')
            msg = self.ard.readline()[0:-2].decode("utf-8")
            print(msg)
            msg = msg.split(',')
            if float(msg[0]) > 0 and float(msg[0]) < 20000:
                self.data['data1'].append([time_true, time_sincestart, float(msg[0])])
            else:
                self.data['data1'].append([time_true, time_sincestart, -1])

            if float(msg[1]) > 0 and float(msg[1]) < 20000:
                self.data['data2'].append([time_true, time_sincestart, float(msg[1])])
            else:
                self.data['data2'].append([time_true, time_sincestart, -1])

            if float(msg[2]) > 0 and float(msg[2]) < 20000:
                self.data['data3'].append([time_true, time_sincestart, float(msg[2])])
            else:
                self.data['data3'].append([time_true, time_sincestart, -1])

            if float(msg[3]) > 0 and float(msg[3]) < 20000:
                self.data['data4'].append([time_true, time_sincestart, float(msg[3])])
            else:
                self.data['data4'].append([time_true, time_sincestart, -1])

            #self.data['data2'].append([time_true,time_sincestart,float(msg[1])])
            #self.data['data3'].append([time_true,time_sincestart,float(msg[2])])
            #self.data['data4'].append([time_true,time_sincestart,float(msg[3])])
        except:
            print('Could not be read correctly')

        if time_true - self.save_timer > 600:
            self.Save()

    # Communicate with Arduino to receive data
    def UpdateGraph(self):
        d1 = [x[2] for x in self.data['data1']]
        d2 = [x[2] for x in self.data['data2']]
        d3 = [x[2] for x in self.data['data3']]
        d4 = [x[2] for x in self.data['data4']]
        d_avg1 = (np.array(d1) + np.array(d2))/2
        d_avg2 = (np.array(d3) + np.array(d4))/2
        try:
            self.display_no = int(self.txt_points.text())
        except:
            self.display_no = 500

        # If length of data is less than specified display, set output to data length
        if len(d1) <= self.display_no:
            self.l1.setData(d1)
            self.l2.setData(d2)
            self.l3.setData(d_avg1)
            self.l4.setData(d3)
            self.l5.setData(d4)
            self.l6.setData(d_avg2)
        # Else, display data points minus the display number to control range
        else:
            self.l1.setData(d1[-self.display_no:])
            self.l2.setData(d2[-self.display_no:])
            self.l3.setData(d_avg1[-self.display_no:])
            self.l4.setData(d3[-self.display_no:])
            self.l5.setData(d4[-self.display_no:])
            self.l6.setData(d_avg2[-self.display_no:])

        self.l1.setVisible(self.data_select1.isChecked())
        self.l2.setVisible(self.data_select1.isChecked())
        self.l3.setVisible(self.data_select3.isChecked() and \
                           self.data_select1.isChecked() or \
                           not self.data_select1.isChecked() and \
                           not self.data_select2.isChecked() and \
                           self.data_select3.isChecked())
        #self.l3.setVisible(not self.data_select1.isChecked() and not self.data_select2.isChecked() and self.data_select3.isChecked())
        self.l4.setVisible(self.data_select2.isChecked())
        self.l5.setVisible(self.data_select2.isChecked())
        self.l6.setVisible(self.data_select3.isChecked() and \
                           self.data_select2.isChecked())
        self.l6.setVisible(self.data_select3.isChecked() and \
                           self.data_select2.isChecked() or \
                           not self.data_select2.isChecked() and \
                           not self.data_select1.isChecked() and \
                           self.data_select3.isChecked())

    def StartRecording(self):
        if self.go_state:
            self.time_start = time.time()
            self.timer.start(100)

    def Reset(self):
        self.data = {
            'data1': [],
            'data2': [],
            'data3': [],
            'data4': [],
            'notes': [[0.0, 0.0, 'start_program']],
        }

    def StopRecording(self):
        self.timer.stop()

    def AddNote(self):
        msg = self.txt_note.text()
        time_true = time.time() - self.time_start_true
        try:
            time_sincestart = time.time() - self.time_start
        except:
            time_sincestart=0

        self.data['notes'].append([time_true,time_sincestart,msg])

    def Save(self):
        print(self.path)
        msg = self.path
        # ar = np.zeros([len(self.data['data1']), 5])
        ar = np.zeros([5, 5])
        # ar[:,0] = [x[0] for x in self.data['data1']]
        # ar[:,1] = [x[2] for x in self.data['data1']]
        # ar[:,2] = [x[2] for x in self.data['data2']]
        # ar[:,3] = [x[2] for x in self.data['data3']]
        # ar[:,4] = [x[2] for x in self.data['data4']]

        with open(msg+'/dummy_data.txt','w+') as f:
            np.savetxt(f,ar,fmt=['%f','%f','%f','%f','%f'])

        # with open(msg+'_notes.txt','w+') as f:
        #     for note in self.data['notes']:
        #         #print(str(note[0]) +' : '+ note[2])
        #         f.write(str(note[0]) +' : '+ note[2]+'\n')

    def ChooseFile(self):
        self.save_file = QtGui.QFileDialog.getSaveFileName()[0]
        self.txt_file.setText(self.save_file)

    def SearchPorts(self):
        active_ports = []
        for number in range(12):
            try:
                verify = serial.Serial('COM' + str(number))
                active_ports.append((number, verify.portstr))
                verify.close()

            except serial.SerialException:
                pass
        return active_ports

    def SetPort(self):
        port = self.com_select.currentText()
        #print(port)
        try:
            self.ard = serial.Serial(
                port=port,
                baudrate=500000,
                timeout=2
            )
            time.sleep(2)
            self.go_state=True
        except:
            #print('no sucessful connection')
            self.go_state=False


class Controller:

    def __init__(self):
        pass

    def show_setup(self):
        # Call first setup window
        self.setup = Setup()
        # Code to call main window
        self.setup.switch_window.connect(self.show_main)
        self.setup.show()

    def show_main(self, pass_value):
        self.window = MainWindow(pass_value)
        self.setup.close()
        self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_setup()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()