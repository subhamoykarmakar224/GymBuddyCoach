from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class TabVersionControl(QWidget):
    def __init__(self):
        super(TabVersionControl, self).__init__()
        # Layouts
        self.vbox = QVBoxLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Main Layout
        self.vbox.addWidget(QLabel('TAB VERSION CONTROL '))

        # Add Main Widget to Parent Layout
        self.setLayout(self.vbox)

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        pass

    def setListeners(self):
        pass