from PyQt4.QtGui import *


class TabHome(QWidget):
    def __init__(self):
        super(TabHome, self).__init__()

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
        self.vbox.addWidget(QLabel('TAB HOME'))

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