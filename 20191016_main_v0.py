# Import general modules
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Import style packages
import qtmodern.styles
import qtmodern.windows

# Import Perlis modules
from class_setup import class_setup_main
from class_mainwindow import class_mainwindow_main
from class_landing import class_landing_main
from class_testwindow import class_testwindow_main


# Passvalue is a list: [0] is a dict with the recipe; [1] is a str with the path
# Define controller to act
class Controller(QtWidgets.QMainWindow):
    """
    Controller switches between program windows.
    """
    def __init__(self):
        super(Controller, self).__init__()
        # Initialize landing window
        self.landing = class_landing_main.landing_window()
        pass

    def show_landing(self):
        try:
            self.main_window.close()
        except:
            pass

        try:
            self.test_window.close()
        except:
            pass

        try:
            self.setup.close()
        except:
            pass
        # Code to call main window
        self.landing.switch_setupwindow.connect(self.show_setup)
        self.landing.switch_testwindow.connect(self.show_test)
        self.landing.show()

    def show_setup(self, pass_value):
        try:
            self.main_window.close()
        except:
            pass

        try:
            self.test_window.close()
        except:
            pass

        try:
            self.landing.close()
        except:
            pass
        # Call first setup window
        self.setup = class_setup_main.setup(pass_value)
        # Code to call main window
        self.setup.switch_landingwindow.connect(self.show_landing)
        self.setup.switch_mainwindow.connect(self.show_main)
        self.setup.show()

    def show_main(self, pass_value):
        self.main_window = class_mainwindow_main.MainWindow(pass_value)
        self.setup.close()
        self.main_window.switch_landingwindow.connect(self.show_landing)
        self.main_window.switch_setupwindow.connect(self.show_setup)
        self.main_window.show()

    def show_test(self):
        self.test_window = class_testwindow_main.TestWindow()
        self.landing.close()
        self.test_window.switch_landingwindow.connect(self.show_landing)
        self.test_window.show()


# Run code
def main():
    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    control = Controller()
    control.show_landing()
    # mw = qtmodern.windows.ModernWindow(controller)
    # mw.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
