from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import sys
import MainWindow as mw
import Configuration as cfg
import GYMMSSystemTray as CustomSystemTray


def startAPP():
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
    trayIcon = CustomSystemTray.GYMMSSystemTray(app)
    trayIcon.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='PyQt5'))
    screen = mw.MainWindowApplication(trayIcon)

    sys.exit(app.exec_())
