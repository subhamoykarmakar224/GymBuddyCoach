from PyQt4.QtGui import *


class TabSettings(QWidget):
    def __init__(self):
        super(TabSettings, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('TAB Settings --->>> '))
        self.setLayout(self.vbox)