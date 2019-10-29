# Test script for main window
# Feeds in predefined path and recipe into the main window for testing

# Import general modules
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Import Perlis modules
import class_mainwindow_main


# Define controller to act
class Controller:

    def __init__(self):
        pass

    def show_main(self, pass_value):
        self.window = class_mainwindow_main.MainWindow(pass_value)
        self.window.show()


# Run code
def main():
    # Define dummy values for passing in
    recipe = {'step_txt': ["ambient", "base", "protein"], 'step_time': ["5", "10", "15"]}
    path = ""
    pass_value = [recipe, path]

    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main(pass_value)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()