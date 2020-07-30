from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import MainWindow as mw

if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash_pix = QPixmap('img/Logo_BIG_blue.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    screen = mw.MainWindowApplication()
    sys.exit(app.exec_())
