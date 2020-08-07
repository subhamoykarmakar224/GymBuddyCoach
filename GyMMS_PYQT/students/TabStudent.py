from PyQt4.QtGui import *


class TabStudent(QWidget):
    def __init__(self):
        super(TabStudent, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('TAB STUDENT --->>> '))
        self.setLayout(self.vbox)