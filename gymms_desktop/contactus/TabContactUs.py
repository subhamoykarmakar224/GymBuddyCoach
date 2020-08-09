from PyQt5.QtWidgets import *


class TabContactUs(QWidget):
    def __init__(self):
        super(TabContactUs, self).__init__()
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
        self.vbox.addWidget(QLabel('TAB CONTACT US'))

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