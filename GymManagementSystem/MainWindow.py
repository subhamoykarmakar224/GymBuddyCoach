from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import WindowTitleBar as windowtitlebar
import SideNavbar as sidenavbar


class MainWindowApplication(QMainWindow):
    def __init__(self):
        super(MainWindowApplication, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle(cfg.APPLICATION_TITLE)
        self.setMinimumSize(1366, 768)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: " + cfg.COLOR_CHARCOAL + ";")

        # Layouts
        vLayout = QVBoxLayout()

        # Sub Layouts
        hLayout = QHBoxLayout()

        # Add to Layout
        vLayout.addWidget(windowtitlebar.WindowTitleBar(self))
        vLayout.addWidget(sidenavbar.SideNavbar())

        # setting central widget
        mainVLayoutWidget = QWidget()
        mainVLayoutWidget.setLayout(vLayout)
        self.setCentralWidget(mainVLayoutWidget)

        self.show()
        self.showMaximized()
