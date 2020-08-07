from PyQt4.QtGui import *
from PyQt4.QtCore import *
import requests, sys
import Configuration as cfg

import accesscontrol.LoginScreen as loginscreen
import sync.AutoSync as autosync
import home.TabHome as tabhome
import students.TabStudent as tabstudent
import notification.TabNotification as tabontif
import settings.TabSettings as tabsettings
# import contactus.TabContactUs as tabcontactus
# import update.TabVersionControl as tabversioncontrol
from CustomMessageBox import *


class MainWindowApplication(QMainWindow):
    def __init__(self, phone):
        super(MainWindowApplication, self).__init__()
        self.phone = phone

        loginStatus = -1
        while loginStatus != 1 or loginStatus != -1000:
            if self.connectedToInternet() != 200:
                self.showConnectToNetErrorMessage()
                loginStatus = -1000
                break

            login = loginscreen.LoginScreen()
            login.exec_()
            loginStatus = login.loginStatus
            if login.loginStatus == -1000:
                break

            if login.loginStatus == -999:
                msgBox = CustomCriticalMessageBox()
                msgBox.setWindowTitle("Error")
                msgBox.setText("Please Login to continue!")
                msgBox.addButton(QMessageBox.Ok)
                msgBox.exec_()
            elif login.loginStatus == 1:
                break

        if loginStatus == 1:
            self.initUi()
            self.syncData()
        else:
            sys.exit(0)

    # check if connected to the internet
    def connectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code

    def showConnectToNetErrorMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        msg.setWindowTitle("Error")
        msg.setText("Please connect to the internet and try again!")
        msg.exec_()

    def initUi(self):
        self.setWindowTitle(cfg.APP_NAME)
        self.setMinimumSize(1280, 720)
        self.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        # self.showMaximized()

        vLayout = QVBoxLayout()

        self.tabsTitle = [
                "Home", "Students", "Notification", "Settings"
            ]
        tabGroup = QTabWidget()
        tabGroup.tabBar().setCursor(Qt.PointingHandCursor)
        vLayout.addWidget(tabGroup)

        tabGroup.addTab(tabstudent.TabStudent(), self.tabsTitle[1])
        tabGroup.addTab(tabhome.TabHome(), self.tabsTitle[0])
        tabGroup.addTab(tabontif.TabNotification(), self.tabsTitle[2])
        tabGroup.addTab(tabsettings.TabSettings(), self.tabsTitle[3])

        # setting central widget
        mainVLayoutWidget = QWidget()
        mainVLayoutWidget.setLayout(vLayout)
        self.setCentralWidget(mainVLayoutWidget)

        self.show()

    def closeEvent(self, event):
        event.accept()

    def syncData(self):
        autosync.AutoSync(self.phone)
