# Import general modules
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Import Perlis modules
import class_setup_main

# Define dummy class just to display the data that is passed on
class NextWindow(QtWidgets.QMainWindow):

    def __init__(self, pass_value):
        super(NextWindow, self).__init__()
        self.setGeometry(50, 50, 600, 300)

        self.experiment_steps = pass_value[0]
        self.path = pass_value[1]

        self.setCentralWidget(QtWidgets.QWidget(self))
        self.layout = QtWidgets.QGridLayout()
        self.centralWidget().setLayout(self.layout)

        self.step1_time = QtWidgets.QLabel(self.experiment_steps["step_txt"][0])
        self.step1_text = QtWidgets.QLabel(self.experiment_steps["step_time"][0])
        self.step2_time = QtWidgets.QLabel(self.experiment_steps["step_txt"][1])
        self.step2_text = QtWidgets.QLabel(self.experiment_steps["step_time"][1])
        self.path_text = QtWidgets.QLabel(self.path)

        self.layout.addWidget(self.step1_time, 1, 1)
        self.layout.addWidget(self.step1_text, 1, 2)
        self.layout.addWidget(self.step2_time, 2, 1)
        self.layout.addWidget(self.step2_text, 2, 2)
        self.layout.addWidget(self.path_text, 3, 2)

        self.show()


# Define controller to act
class Controller:

    def __init__(self):
        pass

    def show_setup(self):
        # Call first setup window
        self.setup = class_setup_main.Setup()
        # Code to call main window
        self.setup.switch_window.connect(self.show_next)
        self.setup.show()

    def show_next(self, pass_value):
        self.window = NextWindow(pass_value)
        self.setup.close()
        self.window.show()


# Run code
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_setup()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()