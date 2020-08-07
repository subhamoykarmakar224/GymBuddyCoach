from PyQt4.QtGui import *


class TabNotification(QWidget):
    def __init__(self):
        super(TabNotification, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('TAB NOTIFICATION --->>> '))
        self.setLayout(self.vbox)