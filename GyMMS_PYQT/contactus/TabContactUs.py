from PyQt4.QtGui import *


class TabContactUs(QWidget):
    def __init__(self):
        super(TabContactUs, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('TAB Contact Us --->>> '))
        self.setLayout(self.vbox)