from PyQt4.QtGui import *
import qdarkstyle
import sys
import MainWindow as mw
import accesscontrol.LoginScreen as loginscreen
import Configuration as cfg


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt4'))
    screen = mw.MainWindowApplication("+919432743720")
    # loginscreen.LoginScreen()
    sys.exit(app.exec_())
