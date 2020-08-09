from PyQt5.QtGui import *
from PyQt5.QtCore import *


def getPixMap(src):
    pixmap = QPixmap(src)
    return pixmap.scaled(24, 24, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)