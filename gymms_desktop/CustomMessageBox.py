from PyQt4.QtGui import *
import Configuration as cfg


def CustomInfoMessageBox():
    msg = QMessageBox()
    msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
    msg.setIcon(QMessageBox.Information)
    return msg


def CustomCriticalMessageBox():
    msg = QMessageBox()
    msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
    msg.setIcon(QMessageBox.Critical)
    return msg



