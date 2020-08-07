from PyQt4.QtGui import *


class TabHome(QWidget):
    def __init__(self):
        super(TabHome, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('TAB Home --->>> '))
        self.setLayout(self.vbox)