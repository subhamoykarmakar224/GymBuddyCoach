from PyQt4.QtGui import *


class TabVersionControl(QWidget):
    def __init__(self):
        super(TabVersionControl, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('TAB Version Control --->>> '))
        self.setLayout(self.vbox)