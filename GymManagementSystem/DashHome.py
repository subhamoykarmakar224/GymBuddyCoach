from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg


# Home Dashboard
class DashHome(QWidget):
    def __init__(self):
        super(DashHome, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main Layout
        vbox = QVBoxLayout(self)

        # Widgets

        # Widget Properties

        # Add to Main Layout
        vbox.addWidget(QLabel("HOME..."))

        # Listeners

        # Add to main layout
        self.setLayout(vbox)
