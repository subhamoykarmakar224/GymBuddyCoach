from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import Configuration as cfg


class GYMMSSystemTray(QSystemTrayIcon):
    def __init__(self, app):
        super(GYMMSSystemTray, self).__init__()
        self.setIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        self.setToolTip("GYMMS")
        self.menuControl()
        self.show()

    def menuControl(self):
        menu = QMenu()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(sys.exit)
        self.setContextMenu(menu)
