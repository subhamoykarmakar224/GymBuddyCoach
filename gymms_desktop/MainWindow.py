from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, sys, os
from Helper import *
import Configuration as cfg
import accesscontrol.LoginScreenSQL as LoginScreenSQL
import accesscontrol.LoginScreenFB as LoginScreenFB


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
    def __init__(self):
        super(MainWindowApplication, self).__init__()
        self.phone = ""

        loginStatus = -1
        lastUserLoginStatus = self.checkLastUserLoginStatus()
        if not lastUserLoginStatus:
            status = self.checkIfAdminsPresent()
            while loginStatus != 1 or loginStatus != -1000:
                if self.connectedToInternet() != 200:
                    self.showConnectToNetErrorMessage()
                    loginStatus = -1000
                    break

                login = loginscreen.LoginScreen(status)
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
        else:
            loginStatus = 1

        if loginStatus == 1:
            self.initUi()
        else:
            sys.exit(0)

    # Checks is atleast one admin present
    def checkIfAdminsPresent(self):
        loginDB = LoginScreenSQL.SQLUserAdmin()
        return loginDB.checkIfUserPresent()

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
        f = open(cfg.TMP_FILE_URL, "r")
        ph = f.read().strip("\n")

        self.userData =  LoginScreenSQL.SQLUserAdmin().getLoggedInData(ph)
        if self.userData[cfg.KEY_ADMIN_ID] == "":
            self.close()

        self.setWindowTitle(cfg.APP_NAME + " Welcome, " + self.userData[cfg.KEY_ADMIN_USERNAME] + "!")
        self.setMinimumSize(1280, 600)
        self.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        self.showMaximized()

        vLayout = QVBoxLayout()

        self.tabsTitle = [
                "Home", "Students", "Notification", "Settings"
            ]
        tabGroup = QTabWidget()
        tabGroup.tabBar().setCursor(Qt.PointingHandCursor)

        # Top Bar
        self.lblUserName = QLabel("Hi! " + self.userData[cfg.KEY_ADMIN_NAME])
        self.layoutSubTitle = QHBoxLayout()
        self.layoutButtonMenu = QHBoxLayout()

        self.lblUserName.setStyleSheet("font-size: 20px;")

        self.btnLogout = QLabel()
        self.btnLogout.setPixmap(getPixMap(cfg.IC_POWER))
        self.btnLogout.setAlignment(Qt.AlignTrailing)
        self.btnLogout.setCursor(Qt.PointingHandCursor)
        self.btnLogout.setToolTip("Logout")
        self.btnLogout.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnLogout.mousePressEvent = self.logoutCurrentUser

        self.layoutButtonMenu.addWidget(self.btnLogout)

        self.layoutSubTitle.addWidget(self.lblUserName)
        self.layoutSubTitle.addWidget(self.btnLogout)

        tabGroup.addTab(tabstudent.TabStudent(), self.tabsTitle[1])
        tabGroup.addTab(tabhome.TabHome(), self.tabsTitle[0])
        tabGroup.addTab(tabontif.TabNotification(), self.tabsTitle[2])
        tabGroup.addTab(tabsettings.TabSettings(), self.tabsTitle[3])

        vLayout.addLayout(self.layoutSubTitle)
        vLayout.addWidget(tabGroup)

        # setting central widget
        mainVLayoutWidget = QWidget()
        mainVLayoutWidget.setLayout(vLayout)
        self.setCentralWidget(mainVLayoutWidget)

        self.show()
        # TODO :: Uncomment later
        # self.syncData()

    def closeEvent(self, event):
        event.accept()

    def syncData(self):
        syncer = autosync.AutoSync()
        syncer.exec_()

    def checkLastUserLoginStatus(self):
        if not os.path.exists(cfg.TMP_FILE_URL):
            return False

        f = open(cfg.TMP_FILE_URL, "r")
        ph = f.read().strip("\n")

        s = LoginScreenSQL.SQLUserAdmin()
        res_db = s.getLoginStatus(ph)

        f = LoginScreenFB.LoginScreenFB()
        res_fb = f.getGymMetaData(ph)

        if res_fb == {}:
            self.forceLogOut()
        else:
            if res_db == 1:
                return True
        return False

    def logoutCurrentUser(self, e):
        s = LoginScreenSQL.SQLUserAdmin()
        if not os.path.exists(cfg.TMP_FILE_URL):
            s.updateAdminLoginStatus(0)
            return

        f = open(cfg.TMP_FILE_URL, "r")
        ph = f.read().strip("\n")

        f = LoginScreenFB.LoginScreenFB()
        res_fb = f.getGymMetaData(ph)

        if res_fb == {}:
            self.forceLogOut()
            return

        msg1 = CustomCriticalMessageBox()
        msg1.setWindowTitle("Alert!")
        msg1.setText("Are you sure you want to logout?")
        msg1.addButton(QMessageBox.Yes)
        msg1.addButton(QMessageBox.No)
        reply = msg1.exec_()

        if reply == QMessageBox.Yes:
            if os.path.isfile(cfg.TMP_FILE_URL):
                os.remove(cfg.TMP_FILE_URL)


            s.updateAdminLoginStatus(0)
            self.close()
            MainWindowApplication()
        else:
            return

    def forceLogOut(self):
        msg1 = CustomCriticalMessageBox()
        msg1.setWindowTitle("Alert!")
        msg1.setText("It seems your status has been blocked. Please speak to your vendor for further information.")
        msg1.exec_()

        if os.path.isfile(cfg.TMP_FILE_URL):
            os.remove(cfg.TMP_FILE_URL)

        s = LoginScreenSQL.SQLUserAdmin()
        s.updateAdminLoginStatus(-1)
        self.close()
        MainWindowApplication()
        return


