import sys, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import accesscontrol.LoginScreen as LoginScreen
import Dashboard as dash


def main():
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))

    # splash_pix = QPixmap(cfg.SPLASH_SCREEN_URL)
    # splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    # splash.show()
    # time.sleep(2)
    # loginScreen = LoginScreen.LoginScreen()
    # splash.finish(loginScreen)
    #
    # app.setStyle(QStyleFactory.create('cleanlooks'))

    dash.Dashboard("+919432743720")
    sys.exit(app.exec_())
