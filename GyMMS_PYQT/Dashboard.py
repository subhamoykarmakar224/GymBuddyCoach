'''
Author @ Subhamoy Karmakar
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import home.TabHome as tabhome
import students.TabStudent as tabstudent
import notification.TabNotification as tabontif
import contactus.TabContactUs as tabcontactus
import settings.TabSettings as tabsettings
import update.TabVersionControl as tabversioncontrol


class Dashboard(QMainWindow):
    def __init__(self, phone):
        super(Dashboard, self).__init__()
        self.phone = phone
        self.initUi(800, 650, 10)

    def initUi(self, winWidth, winHeight, winMargins):
        self.setWindowTitle(cfg.APP_NAME)
        self.setMinimumSize(800, 650)

        vLayout = QVBoxLayout()

        # self.tabsTitle = []
        # for tab in cfg.TABS:
        #     self.tabsTitle.append(tab[1])

        # tabGroup = QTabWidget()
        # tabGroup.tabBar().setCursor(Qt.PointingHandCursor)
        # vLayout.addWidget(tabGroup)

        # tabGroup.addTab(upload.UploadLogs(), self.tabsTitle[0])
        # tabGroup.addTab(view.ViewLogs(), self.tabsTitle[1])
        # tabGroup.addTab(visualize.VisualizationLogs(), self.tabsTitle[2])
        # tabGroup.addTab(report.ReportLogs(), self.tabsTitle[3])

        vLayout.addWidget(QLabel("TEST"))

        # setting central widget
        mainVLayoutWidget = QWidget()
        mainVLayoutWidget.setLayout(vLayout)
        self.setCentralWidget(mainVLayoutWidget)

        self.showMaximized()
        self.show()

    # def aboutClick(self):
    #     splash_pix = QPixmap(cfg.SPLASH_SCREEN_URL)
    #     # splash_pix.scaled(732, 309)
    #     self.splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    #     self.splash.mousePressEvent = self.splashClicked
    #     self.splash.show()