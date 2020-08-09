from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import qdarkstyle
import sys
import MainWindow as mw
import Configuration as cfg


def startAPP():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='PyQt5'))
    screen = mw.MainWindowApplication()
    sys.exit(app.exec_())
