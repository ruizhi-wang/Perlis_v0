# Import general modules
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# Minor edit

# Import Perlis modules
from class_setup import class_setup_main
from class_mainwindow import class_mainwindow_main

# Comment dummy

# Define controller to act
class Controller:

    def __init__(self):
        pass

    def show_setup(self):
        # Call first setup window
        self.setup = class_setup_main.Setup()
        # Code to call main window
        self.setup.switch_window.connect(self.show_main)
        self.setup.show()

    def show_main(self, pass_value):
        self.window = class_mainwindow_main.MainWindow(pass_value)
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