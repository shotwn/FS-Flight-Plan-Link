from PySide2.QtWidgets import QApplication
from gui.main_window import MainWindow


class GUI:
    def __init__(self, fslapp):
        self.fslapp = fslapp
        self.app = QApplication([])
        self.main_window = MainWindow(self)

    def start(self):
        """ BLOCKING """
        self.main_window.show()
        self.app.exec_()
