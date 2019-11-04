import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
import numpy as np
import serial
import time

# Comment to check
# Another comment to check

class MainWindow(QtWidgets.QMainWindow):

    switch_landingwindow = QtCore.pyqtSignal()
    switch_setupwindow = QtCore.pyqtSignal(list)

    def __init__(self, pass_value):
        super(MainWindow, self).__init__()

        self.setGeometry(50, 50, 800, 600)

        self.setWindowTitle('HexagonFab Analysis App - Protocol Experiment')
        self.setWindowIcon(QtGui.QIcon('HexFab_logo.png'))

        #--------------------------------------------------------------------------------------------------------------
        # Helper variables
        # Initialize the time counter for displaying the remaining time of the step
        self.counter = 0
        # Initialize the time counter for displaying the remaining time of the step
        self.save_counter = 0
        # Initialize step counter
        self.step_tracker = 0
        # Load values in form arguments
        self.recipe = pass_value[0]
        self.path = pass_value[1]
        
        # Set go_state to False to prevent data being written
        self.go_state = False  # Create class variables (i.e. go_state) and set it to

        # Set timer for saving to 0
        self.save_timer = 0

        # Set initial baseline value
        self.baseline = [1, 1, 1, 1]
        
        # Setting up the data sets for saving and displaying
        self.data = {
            'data1': [],
            'data2': [],
            'data3': [],
            'data4': [],
            'notes': [[0.0, 0.0, 'start_program']],
        }

        self.display_no = 500  # Initial amount of data points displayed


        # Populate tool bar
        self.toolBar = self.addToolBar('Create')

        # self.returnHome = QtWidgets.QAction('Back', self)
        # self.returnHome.triggered.connect(self.PopUpHome)
        # self.toolBar.addAction(self.returnHome)

        self.returnRecipe = QtWidgets.QAction('< Back', self)
        self.returnRecipe.triggered.connect(self.PopUpSetup)
        self.toolBar.addAction(self.returnRecipe)

        self.closeWindow = QtWidgets.QAction('Close', self)
        self.closeWindow.triggered.connect(self.PopUpClose)
        self.toolBar.addAction(self.closeWindow)


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

    def widgets(self):

        # HexagonFab Top Label
        self.header_label = QtGui.QLabel('HexagonFab')
        pixmap = QPixmap('./class_landing/hexagonfab_logo_250.png')
        pixmap = pixmap.scaledToWidth(100, 1)
        self.header_label.setPixmap(pixmap)


        # Protocol plan
        self.lbl_recipe = QtGui.QLabel('Protocol')
        self.lbl_recipe.setStyleSheet('font-weight: bold; padding-top:8;')

        # Controls
        self.control_label = QtGui.QLabel('Experiment Control')
        self.control_label.setStyleSheet('font-weight: bold; padding-top:8;')

        # Reader & sensor connection
        self.settings_label = QtGui.QLabel('Reader & sensor connection')
        self.settings_label.setStyleSheet('font-weight: bold; padding-top:8;')


        # Start connection & showing the graph
        self.btn_connect = QtGui.QPushButton('Connect \n sensor')  # Create instance of QPushButton
        self.btn_connect.setStyleSheet("height: 50")
        self.btn_connect.setFixedWidth(80)
        self.btn_connect.clicked.connect(self.ConnectSensor)  # Call StartShowing function when start button pressed
        self.btn_connect.clicked.connect(self.PopUpConnect)  # Call popup function when start button pressed

        # Operating the experiment
        self.btn_start = QtGui.QPushButton('Start Experiment')  # Create instance of QPushButton
        self.btn_start.setStyleSheet("background-color: #4933FF; color: white; height: 20;")
        self.btn_start.setFixedWidth(150)
        self.btn_start.pressed.connect(self.PopUpStart)  # Activate warning about experiment erased
        self.btn_stop = QtGui.QPushButton('Stop')
        self.btn_stop.setStyleSheet("height: 20;")
        self.btn_stop.setFixedWidth(80)
        self.btn_stop.clicked.connect(self.StopRecording)  # Call StopRecording function at button press
        self.btn_reset = QtGui.QPushButton('Reset')
        self.btn_reset.setStyleSheet("height: 20;")
        self.btn_reset.setFixedWidth(80)
        self.btn_reset.clicked.connect(self.PopUpReset)  # Call Reset function at button press
        self.btn_baseline = QtGui.QPushButton('Baseline')
        self.btn_baseline.setStyleSheet("height: 20;")
        self.btn_baseline.setFixedWidth(80)
        self.btn_baseline.clicked.connect(self.BaseValue)  # Call Reset function at button press


        # Label showing the experimental steps
        self.current_time_counter = QtWidgets.QLabel("Time remaining \n -")
        self.duration_counter = QtWidgets.QLabel("Time \n -")
        self.step_counter = QtWidgets.QLabel("Current step \n -")
        self.duration_next = QtWidgets.QLabel()
        self.step_next = QtWidgets.QLabel()

        # Buttons to navigate the experiments
        self.btn_experiment = QtWidgets.QPushButton("next step >")
        self.btn_experiment.pressed.connect(self.StepExperiment) # Trigger next step in experimetn
        # Note text and connection
        self.txt_note = QtGui.QLineEdit('Write note...')  # Create instance of QLineEdit
        self.btn_note = QtGui.QPushButton('Add note')  # Create instance of QPushButton
        self.btn_note.setFixedWidth(80)
        self.btn_note.clicked.connect(self.AddNote)  # Call AddNote function at button press

        # Save, file and text widgets and connections
        # self.txt_file = QtGui.QLineEdit('file_name')  # Create instance of QLineEdit
        # self.btn_save = QtGui.QPushButton('save')  # Create instance of QPushButton
        # self.btn_save.clicked.connect(self.Save)  # Call Save function at button press
        # self.btn_file = QtGui.QPushButton('file...')  # Create instance of QPushButton
        # self.btn_file.clicked.connect(self.ChooseFile)  # Call ChooseFile function at button press

        # What - data widgets
        self.data_select1 = QtGui.QCheckBox('Sensor1')  # Create instance of QCheckBox
        self.data_select2 = QtGui.QCheckBox('Sensor2')  # Create instance of QCheckBox
        self.data_select3 = QtGui.QCheckBox('Averages')  # Create instance of QCheckBox

        # Select the comport
        self.com_label = QtGui.QLabel('Com Port')  # Create instance of QLabel
        self.com_select = QtGui.QComboBox()  # Create instance of QComboBox
        for port in ['COM' + str(x) for x in range(12)]:
            self.com_select.addItem(port)  # Call Qt function addItem on self.com_select
        # XXXX
        self.com_select.currentIndexChanged.connect(self.SetPort)  # Call SetPort function to select com port
        # XXXX

        self.com_select.setFixedWidth(70)

        # No-points box
        self.points_label = QtGui.QLabel('No data points')  # Create instance of QLabel
        self.txt_points = QtGui.QLineEdit('500')  # Create instance of QLineEdit
        self.txt_points.setFixedWidth(70)

        # Define table
        self.recipeTable = QTableWidget()
        # self.currentTable = QTableWidget()

        # # Comport select
        # self.com_label = QtGui.QLabel('Com Port : ')  # Create instance of QLabel
        # self.com_select = QtGui.QComboBox()  # Create instance of QComboBox
        # for port in ['COM' + str(x) for x in range(12)]:
        #     self.com_select.addItem(port)  # Call Qt function addItem on self.com_select
        # self.com_select.currentIndexChanged.connect(self.SetPort)  # Call SetPort function to select com port

        # Plot widgets and lines
        self.plot = pg.PlotWidget()
        self.l1 = self.plot.plot(pen=pg.mkPen('r', width=3))
        self.l2 = self.plot.plot(pen=pg.mkPen('b', width=3))
        self.l3 = self.plot.plot(pen=pg.mkPen('w', width=3))
        self.l4 = self.plot.plot(pen=pg.mkPen('r', width=3, style=QtCore.Qt.DashLine))
        self.l5 = self.plot.plot(pen=pg.mkPen('b', width=3, style=QtCore.Qt.DashLine))
        self.l6 = self.plot.plot(pen=pg.mkPen('w', width=3, style=QtCore.Qt.DashLine))

        # --------------------------------------------

    def generate_recipe_table(self):
        # Create table
        self.recipeTable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.recipeTable.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.recipeTable.setRowCount(len(self.recipe['step_txt']))
        self.recipeTable.setColumnCount(2)
        self.recipeTable.resizeRowsToContents()

        self.recipeTable.setHorizontalHeaderLabels(['Steps', 'Duration'])
        # self.recipeTable.horizontalHeaderItem().setTextAlignment(QtGui.AlignHCenter)
        header = self.recipeTable.horizontalHeader()
        header.setResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setResizeMode(1, QtWidgets.QHeaderView.Stretch)

        for row in range(len(self.recipe['step_txt'])):
            self.recipeTable.setItem(row, 0, QTableWidgetItem(self.recipe['step_txt'][row]))
            self.recipeTable.setItem(row, 1, QTableWidgetItem(self.recipe['step_time'][row]))
            row += 1
        self.show()

    def display_widgets(self):

        # Header label
        self.layout.addWidget(self.header_label, 0, 0)


        # Sidebar - Protocol

        self.layout.addWidget(self.recipeTable, 2, 0, 1, 1)

        # Sidebar - Protocol nav info
        self.layout.addWidget(self.lbl_recipe, 3,0,1,1)
        self.layout.addWidget(self.step_counter, 4, 0)
        self.layout.addWidget(self.duration_counter, 5, 0)
        self.layout.addWidget(self.current_time_counter, 6, 0)
        self.layout.addWidget(self.btn_experiment, 7, 0)

        # Main Window - Plot
        self.layout.addWidget(self.plot,2 ,1 ,1 ,4)  # Add plot (int row, int column, int rowSpan, int columnSpan)

        # Main Window - Control experiment
        self.layout.addWidget(self.control_label, 3, 1)

        self.layout.addWidget(self.btn_stop, 4, 1)
        self.layout.addWidget(self.btn_start, 4, 1, 1, 4, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.btn_reset, 4, 4, QtCore.Qt.AlignRight)
        self.layout.addWidget(self.btn_baseline, 4, 3, QtCore.Qt.AlignRight)

        self.layout.addWidget(self.txt_note, 5, 1, 1, 3)
        self.layout.addWidget(self.btn_note, 5, 4)

        # Main Window - Reader & Sensor connection
        self.layout.addWidget(self.settings_label, 6,1)

        self.layout.addWidget(self.data_select1, 7, 1)
        self.layout.addWidget(self.data_select2, 8, 1)
        self.layout.addWidget(self.data_select3, 9, 1)

        self.layout.addWidget(self.txt_points, 7, 2)
        self.layout.addWidget(self.points_label, 7, 3, QtCore.Qt.AlignLeft)

        self.layout.addWidget(self.com_select, 8, 2)
        self.layout.addWidget(self.com_label, 8, 3, QtCore.Qt.AlignLeft)

        self.layout.addWidget(self.btn_connect, 7, 4,3,1)

        # Style
        self.step_counter.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.duration_counter.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.current_time_counter.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)


        # self.layout.addWidget(self.btn_file, 4, 2)
        # self.layout.addWidget(self.txt_file, 4, 0, 1, 2)
        # self.layout.addWidget(self.btn_save, 4, 3)
        # --------------------------------------------

        # Assign widget locations based on grid layout


        # self.layout.addWidget(self.duration_next, 7, 5)
        # self.layout.addWidget(self.step_next, 7, 3)
        # self.layout.addWidget(self.currentTable, 3, 0, 1, 3)


        # self.generate_current_table()
        self.generate_recipe_table()
        self.BtnDisable()

        self.show()

    def timer_countdown_counter(self):
        # Timer to keep track of time passed for each period
        self.timer_countdown = QtCore.QTimer()
        self.timer_countdown.setInterval(1000)
        self.timer_countdown.timeout.connect(self.recurring_timer)
        self.timer_countdown.start()

    def timer_step_counter(self):
        self.timer_step = QtCore.QTimer()
        step_time= int(self.recipe["step_time"][self.step_tracker]) * 1000
        self.timer_step.setInterval(step_time)
        self.timer_step.timeout.connect(self.PopUpStep)
        self.timer_step.start()

    def recurring_timer(self):
        self.counter -= 1
        self.current_time_counter.setText("Time remaining \n" + str(self.counter))

    def StepExperiment(self):
        num_steps = len(self.recipe["step_time"])

        # Timers stated here in case there are still experimental steps left
        if self.step_tracker < num_steps:
            self.timer_countdown_counter()
            # Get index of current step
            self.counter = int(self.recipe["step_time"][self.step_tracker])
            self.timer_step_counter()
        else:
            self.timer_countdown_counter()
            self.timer_countdown.stop()
            self.current_time_counter.setText("Time remaining \n End")

        # Display information about the correct step
        if self.step_tracker < num_steps:
            # Display information about current step
            self.step_counter.setText("Current step: \n" + self.recipe["step_txt"][self.step_tracker])
            self.duration_counter.setText(
                "Time: \n" + self.recipe["step_time"][self.step_tracker])
        else:
            self.step_counter.setText("Current step \n End")
            self.duration_counter.setText("Time \n End")

        if self.step_tracker + 1 < num_steps:
            # Display information about next step
            self.step_next.setText("Name of next step: " + self.recipe["step_txt"][self.step_tracker + 1])
            self.duration_next.setText("Duration of next step: " + self.recipe["step_time"][self.step_tracker + 1])
        else:
            self.step_next.setText("Current step \n End of Experiment")
            self.duration_next.setText("Time \n End of Experiment")

        self.step_tracker += 1

    # Communicate with Arduino to receive data
    def UpdateData(self):
        time_true = time.time() - self.time_start_true
        # Hotfix for start data since pressing the "start" button
        time_sincestart = time.time() - self.time_start_true

        try:
            self.ard.write(b'1')
            msg = self.ard.readline()[0:-2].decode("utf-8")
            print(msg)
            msg = msg.split(',')
            self.save_counter +=1

            if float(msg[0]) > 0 and float(msg[0]) < 20000:
                self.data['data1'].append([time_true, time_sincestart, float(msg[0])]) # Definition of self.data
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

            # self.data['data2'].append([time_true,time_sincestart,float(msg[1])])
            # self.data['data3'].append([time_true,time_sincestart,float(msg[2])])
            # self.data['data4'].append([time_true,time_sincestart,float(msg[3])])
        except:
            print('Update Data could not be read correctly')

        if self.save_state:
            if time_true - self.save_timer > 1:
                if self.save_counter > 20:
                    self.Save()
                    print('saved')
                    self.save_counter=0

    # Communicate with Arduino to receive data
    def UpdateGraph(self):
        d1 = np.array([x[2] for x in self.data['data1']])/self.baseline[0] # x[2] is an array with all the values recorded for channel 1
        d2 = np.array([x[2] for x in self.data['data2']])/self.baseline[1]
        d3 = np.array([x[2] for x in self.data['data3']])/self.baseline[2]
        d4 = np.array([x[2] for x in self.data['data4']])/self.baseline[3]
        d_avg1 = (np.array(d1) + np.array(d2)) / 2
        d_avg2 = (np.array(d3) + np.array(d4)) / 2

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
        # self.l3.setVisible(not self.data_select1.isChecked() and not self.data_select2.isChecked() and self.data_select3.isChecked())
        self.l4.setVisible(self.data_select2.isChecked())
        self.l5.setVisible(self.data_select2.isChecked())
        self.l6.setVisible(self.data_select3.isChecked() and \
                           self.data_select2.isChecked())
        self.l6.setVisible(self.data_select3.isChecked() and \
                           self.data_select2.isChecked() or \
                           not self.data_select2.isChecked() and \
                           not self.data_select1.isChecked() and \
                           self.data_select3.isChecked())

    def BaseValue(self):
        d1 = np.array([x[2] for x in self.data['data1']])
        d2 = np.array([x[2] for x in self.data['data2']])
        d3 = np.array([x[2] for x in self.data['data3']])
        d4 = np.array([x[2] for x in self.data['data4']])

        len_d1 = len(d1)
        len_d2 = len(d2)
        len_d3 = len(d3)
        len_d4 = len(d4)

        print(np.average(d1[len_d1-10:len_d1]))
        print(np.average(d2[len_d2 - 10:len_d2]))
        print(np.average(d3[len_d3 - 10:len_d3]))
        print(np.average(d4[len_d4 - 10:len_d4]))

        self.baseline = [np.average(d1[len_d1-10:len_d1]), np.average(d2[len_d2 - 10:len_d2]), np.average(d3[len_d3 - 10:len_d3]), np.average(d4[len_d4 - 10:len_d4])]


    def ConnectSensor(self):
        # Timer to data collect
        self.timer = QtCore.QTimer()  # Create QTimer instance
        self.timer.timeout.connect(self.UpdateData)  # Update data at constant time intervals
        self.timer.timeout.connect(self.UpdateGraph)  # Update UI graph at constant time intervals
        
        # Start communication with port
        # Bug: When window closed directly with 'x' button and the port has not been closed before
        # the port remains open and cannot be addressed
        try:
            self.ard = serial.Serial(
                port=self.port,
                baudrate=500000,
                timeout=2
            )
            time.sleep(2)
            self.go_state = True
            print('port set')
        except:
            self.go_state = False
            print('port NOT set')
        
        if self.go_state:
            self.time_start = time.time()
            self.time_start_true = time.time()  # Fix start time (i.e. so that difference with timer gives time passed)
            self.timer.start(100)
            self.save_state = False

    def StartRecording(self):
        if self.go_state:
            self.time_start = time.time()
            self.time_start_true = time.time()  # Fix start time (i.e. so that difference with timer gives time passed)
            self.timer.start(100)
            self.save_state = True
            
    def StopRecording(self):
        self.timer.stop()
        self.ard.close()

        try:
            # Stop step timer in case it has already been triggered
            self.timer_step.stop()
            # Stop countdown timer
            self.timer_countdown.stop()
        except:
            pass

    def Reset(self):
        # Reset plot
        self.l1.setData([0.0])
        self.l2.setData([0.0])
        self.l3.setData([0.0])
        self.l4.setData([0.0])
        self.l5.setData([0.0])
        self.l6.setData([0.0])

        # Stop time
        # Stop global timer
        try:
            self.timer.stop()
        except:
            pass
        try:
            # Stop popup timer
            self.timer_step.stop()
            # Stop countdown timer
            self.timer_countdown.stop()
        except:
            pass

        # Close port
        try:
            self.ard.close()
        except:
            pass

        self.go_state = False
        self.save_state = False

        # Stop plotting
        self.data = {
            'data1': [],
            'data2': [],
            'data3': [],
            'data4': [],
            'notes': [[0.0, 0.0, 'start_program']],
        }

        # Reset Protocol
        self.step_tracker = 0  # Set step tracker to 0 to run Protocol from start

        self.current_time_counter.setText("")
        self.duration_counter.setText("")
        self.step_counter.setText("")
        self.duration_next.setText("")
        self.step_next.setText("")
        
        self.baseline = [1, 1, 1, 1] 

        # Disable all buttons except connect
        self.BtnDisable()

        print("reset performed")
    
    def Save(self):
        msg = self.path
        ar = np.zeros([len(self.data['data1']),5])
        ar[:,0] = [x[0] for x in self.data['data1']]
        ar[:,1] = [x[2] for x in self.data['data1']]
        ar[:,2] = [x[2] for x in self.data['data2']]
        ar[:,3] = [x[2] for x in self.data['data3']]
        ar[:,4] = [x[2] for x in self.data['data4']]

        with open(msg+'_data.txt','w+') as f:
            np.savetxt(f,ar,fmt=['%f','%f','%f','%f','%f'])

        with open(msg+'_notes.txt','w+') as f:
            for note in self.data['notes']:
                f.write(str(note[0]) +' : '+ note[2]+'\n')

    def AddNote(self):
        msg = self.txt_note.text()

        try:
            time_true = time.time() - self.time_start_true
            time_sincestart = time.time() - self.time_start
        except:
            time_true = 0
            time_sincestart = 0

        self.data['notes'].append([time_true, time_sincestart, msg])

    def switch_landing(self):
        self.switch_landingwindow.emit()

    def switch_setup(self):
        pass_val = [self.recipe, self.path]
        self.switch_setupwindow.emit(pass_val)

    # -------------------------------------------------------------------------------------------------------------------
    # Arduino communication

    def SetPort(self):
        self.port = self.com_select.currentText()
        print(self.port)


    # -------------------------------------------------------------------------------------------------------------------
    # Definition of PopUps
    def PopUpConnect(self):
#        resistance_list=self.resistance_val.split(',')
        # text_message = "Sensor resistance values \n"\
        #                +"Sensor 1 - Ch1: "+resistance_list[0]+"\n"+"Sensor 1 - Ch2: "+resistance_list[1]+"\n"+"Sensor 2 - Ch3: "+resistance_list[2]+"\n"+"Sensor 2 - Ch4: "+resistance_list[3]

        if self.go_state:
            msg = self.ard.readline()[0:-2].decode("utf-8")
            print(msg)
            text_message = "Sensor resistance values: " + msg
        else:
            msg = "incorrect com-port"
            text_message = msg

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok:
            if self.go_state:
                self.BtnEnable()

    def PopUpStep(self):
        try:
            # Stop timer, which is counting down the time until the next popup with a command
            self.timer_step.stop()

            current_step = self.step_tracker

            # Define text in message box
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            # For some weird reason, but the time self.step_tracker has been passed in, it has already increased by 1
            if current_step < len(self.recipe["step_time"]):
                msgBox.setText(str(self.recipe["step_txt"][current_step]))

            if current_step == len(self.recipe["step_time"]):
                msgBox.setText("Done with the experiment!")

            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.StepExperiment()

        except:
            pass

    def PopUpEnd(self):
        text_message = "End of experiment"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()

    def PopUpStart(self):
        text_message = "Start Experiment - All previous data will be erased"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok:
            self.StartRecording() # Call StartRecording function when ok button pressed
            self.StepExperiment() # Trigger first step in experiment
        
    def PopUpReset(self):
        text_message = "All data will be erased"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_message)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()
        
        if returnValue == QMessageBox.Ok:
            self.Reset()

    def PopUpHome(self):
        choice = QtWidgets.QMessageBox.question(self, 'Return', 'Are you sure you wish to return to Home?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.switch_landing()
        else:
            pass

    def PopUpSetup(self):
        choice = QtWidgets.QMessageBox.question(self, 'Return', 'Are you sure you wish to return to Protocol Setup?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.switch_setup()
        else:
            pass

    def PopUpClose(self):
        choice = QtWidgets.QMessageBox.question(self, 'Close', 'Are you sure you wish to exit?',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.Reset()
            sys.exit()
        else:
            pass


        # __________________________________________________________________________
            
    def BtnEnable(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.btn_reset.setEnabled(True)
        self.btn_experiment.setEnabled(True)

    def BtnDisable(self):
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_reset.setEnabled(False)
        # self.btn_experiment.setEnabled(False)