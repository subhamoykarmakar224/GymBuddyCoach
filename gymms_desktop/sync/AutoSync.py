from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import requests


class AutoSync(QDialog):
    def __init__(self, phone):
        super(AutoSync, self).__init__()
        self.phone = phone
        self.done = False
        self.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        self.setWindowTitle("Syncing Data...")
        self.setMinimumWidth(500)
        # self.closeEvent = self.closeDialogEvent

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblInProgress = QLabel("Fetching data...")
        self.progress = QProgressBar()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout

        # Add to Main Layout
        self.mainLayout.addWidget(self.lblInProgress, 0, 0)
        self.mainLayout.addWidget(self.progress, 1, 0)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

        self.exec_()

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        pass

    def setListeners(self):
        pass

    # Override :: Stop dialog close till the database is being updated
    def closeEvent(self, event):
        if not self.done:
            event.ignore()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
            msg.setWindowTitle("Error")
            msg.setText("Please wait while we index your database.")
            msg.exec_()
        else:
            self.close()

    # Override :: Stop dialog close when escape is clicked
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if not self.done:
                event.ignore()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
                msg.setWindowTitle("Error")
                msg.setText("Please wait while we index your database.")
                msg.exec_()
            else:
                self.close()

    def connectedToInternet(self):
        # url = 'https://jsonplaceholder.typicode.com/todos/1'
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)

        return res.status_code

    def startSync(self):
        pass
