2019# Reader software script written by Oliver Burton
# Receives Arduino values for resistance across four graphene channels
# Annotated by Lukas Vasadi in June 2019
# Additional annotation by Ruizhi Wang October 2019

# Import Python modules
# 'from...import...' allows named module functions to be referenced directly
# 'as' allows module aliasing to abbreviate long names
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import numpy as np
import serial
import time
import sys                                              # Only needed for command line arguments


# Define new class for readout device
class ReadOut:
    def __init__(self):                                 # Think of __init__ as 'initialize' 
        '''
        '''
        self.go_state = False                           # Create class variables (i.e. go_state)
        self.save_timer = 0
        try:
            #self.ard = serial.Serial(
            #    port='COM1',
            #    baudrate=500000,
            #    timeout=2
            #)
            time.sleep(2)                               # Pause execution for 2 seconds
            self.go_state = False
        except:
            self.go_state = False
        # Setting up the data sets for saving and displaying
        self.data = {
            'data1':[],
            'data2':[],
            'data3':[],
            'data4':[],
            'notes':[[0.0, 0.0, 'start_program']],
        }
        self.time_start_true = time.time()              # Number of seconds since time epoch
        self.display_no = 500                           # Initial amount of data points displayed

        self.app = QtGui.QApplication([])               # QApplication holds the event loop (core loop) of the application
        self.w = QtGui.QWidget()                        # Initialize widgets

        # Timer to data collect
        self.timer = QtCore.QTimer()                    # Create QTimer instance
        self.timer.timeout.connect(self.UpdateData)     # Update data at constant time intervals
        self.timer.timeout.connect(self.UpdateGraph)    # Update UI graph at constant time intervals

        # Layout
        self.lo = QtGui.QGridLayout()                   # Create instance of QGridLayout
        self.w.setLayout(self.lo)                       # Initialize UI grid layout

        # Widgets
        self.Widgets()                                  # Call function Widgets() on self
        self.AddWidgets()                               # Call function AddWidgets() on self

        self.w.show()                                   # Display main window with widgets
        self.app.exec_()                                # Start the event loop
        #print(QtGui.QFileDialog.getSaveFileName())

    def Widgets(self):
        # Start and stop button and connection
        self.btn_start = QtGui.QPushButton('start')                 # Create instance of QPushButton
        self.btn_start.clicked.connect(self.StartRecording)         # Call StartRecording function when start button pressed
        self.btn_stop = QtGui.QPushButton('stop')               
        self.btn_stop.clicked.connect(self.StopRecording)           # Call StopRecording function at button press
        self.btn_reset = QtGui.QPushButton('Reset')
        self.btn_reset.clicked.connect(self.Reset)                  # Call Reset function at button press

        # Note text and connection
        self.txt_note = QtGui.QLineEdit('note')                     # Create instance of QLineEdit
        self.btn_note = QtGui.QPushButton('add note')               # Create instance of QPushButton
        self.btn_note.clicked.connect(self.AddNote)                 # Call AddNote function at button press

        # Save, file and text widgets and connections
        self.txt_file = QtGui.QLineEdit('file_name')                # Create instance of QLineEdit
        self.btn_save = QtGui.QPushButton('save')                   # Create instance of QPushButton
        self.btn_save.clicked.connect(self.Save)                    # Call Save function at button press
        self.btn_file = QtGui.QPushButton('file...')                # Create instance of QPushButton
        self.btn_file.clicked.connect(self.ChooseFile)              # Call ChooseFile function at button press

        # What - data widgets
        self.data_select1 = QtGui.QCheckBox('Sensor1')              # Create instance of QCheckBox
        self.data_select2 = QtGui.QCheckBox('Sensor2')              # Create instance of QCheckBox
        self.data_select3 = QtGui.QCheckBox('Averages')             # Create instance of QCheckBox

        # No-points box
        self.points_label = QtGui.QLabel('No data points : ')       # Create instance of QLabel
        self.txt_points = QtGui.QLineEdit('500')                    # Create instance of QLineEdit

        # Comport select
        self.com_label = QtGui.QLabel('Com Port : ')                # Create instance of QLabel
        self.com_select = QtGui.QComboBox()                         # Create instance of QComboBox
        for port in ['COM' + str(x) for x in range(12)]:        
            self.com_select.addItem(port)                           # Call Qt function addItem on self.com_select
        self.com_select.currentIndexChanged.connect(self.SetPort)   # Call SetPort function to select com port


        # Plot widgets and lines
        self.plot = pg.PlotWidget()
        self.l1 = self.plot.plot(pen=pg.mkPen('r', width=3))
        self.l2 = self.plot.plot(pen=pg.mkPen('b', width=3))
        self.l3 = self.plot.plot(pen=pg.mkPen('w', width=3))
        self.l4 = self.plot.plot(pen=pg.mkPen('r', width=3, style=QtCore.Qt.DashLine))
        self.l5 = self.plot.plot(pen=pg.mkPen('b', width=3, style=QtCore.Qt.DashLine))
        self.l6 = self.plot.plot(pen=pg.mkPen('w', width=3, style=QtCore.Qt.DashLine))

    def AddWidgets(self):
        # Build all widgets and set locations
        self.lo.addWidget(self.btn_start, 1, 3)
        self.lo.addWidget(self.btn_stop, 0, 3)
        self.lo.addWidget(self.btn_reset,2,3)

        self.lo.addWidget(self.points_label, 0,0)
        self.lo.addWidget(self.txt_points, 0, 1)

        self.lo.addWidget(self.data_select1,0,2)
        self.lo.addWidget(self.data_select2,1,2)
        self.lo.addWidget(self.data_select3,2,2)

        self.lo.addWidget(self.com_select,1,1)
        self.lo.addWidget(self.com_label,1,0)

        #self.lo.addWidget(self.btn_note, 1, 1)
        self.lo.addWidget(self.btn_note, 2, 1)
        self.lo.addWidget(self.txt_note, 2, 0)
        #layout.addWidget(listw, 3, 0)
        self.lo.addWidget(self.plot, 3, 0, 1, 4)                    # Add plot (int row, int column, int rowSpan, int columnSpan)

        self.lo.addWidget(self.btn_file,4,2)
        self.lo.addWidget(self.txt_file,4,0,1,2)
        self.lo.addWidget(self.btn_save,4,3)


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
        msg = self.txt_file.text()
        ar = np.zeros([len(self.data['data1']), 5])
        ar[:,0] = [x[0] for x in self.data['data1']]
        ar[:,1] = [x[2] for x in self.data['data1']]
        ar[:,2] = [x[2] for x in self.data['data2']]
        ar[:,3] = [x[2] for x in self.data['data3']]
        ar[:,4] = [x[2] for x in self.data['data4']]

        with open(msg+'_data.txt','w+') as f:
            np.savetxt(f,ar,fmt=['%f','%f','%f','%f','%f'])

        with open(msg+'_notes.txt','w+') as f:
            for note in self.data['notes']:
                #print(str(note[0]) +' : '+ note[2])
                f.write(str(note[0]) +' : '+ note[2]+'\n')


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


if __name__ == '__main__':
    a = ReadOut()
