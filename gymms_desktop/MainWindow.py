from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, sys, os, time, datetime

from Helper import *
import Configuration as cfg
import accesscontrol.LoginScreenSQL as LoginScreenSQL
import accesscontrol.LoginScreenFB as LoginScreenFB
import accesscontrol.LoginScreen as loginscreen
import sync.AutoSync as autosync
import sync.SQLAutoSync as SQLAutoSync
import home.TabHome as tabhome
import students.TabStudent as tabstudent
import notification.TabNotification as tabontif
import settings.TabSettings as tabsettings
from CustomMessageBox import *
import home.FBTabHome as FBTabHome
import home.SQLTabHome as SQLTabHome


class MainWindowApplication(QMainWindow):
    def __init__(self, tray):
        super(MainWindowApplication, self).__init__()
        self.phone = ""
        self.tray = tray
        self.thread = ThreadLiveSoftwareDataControl(self.tray)
        self.thread.force_logout.connect(self.forceLogOutToExtendMembership)
        self.thread.start()
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
        self.showCustomNotification("Welcome!", "Welcome to GYMMS.", 400)
        self.showSplashScreen()
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
        self.tabGroup = QTabWidget()
        self.tabGroup.tabBar().setCursor(Qt.PointingHandCursor)

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

        # self.tabGroup.addTab(tabhome.TabHome(self.tray), self.tabsTitle[0])
        # self.tabGroup.addTab(tabstudent.TabStudent(self.tray), self.tabsTitle[1])
        # self.tabGroup.addTab(tabontif.TabNotification(self.tray), self.tabsTitle[2])
        # self.tabGroup.addTab(tabsettings.TabSettings(), self.tabsTitle[3])

        self.tabGroup.addTab(tabhome.TabHome(self.tray), self.tabsTitle[0])
        self.tabGroup.addTab(tabstudent.TabStudent(self.tray), self.tabsTitle[1])
        self.tabGroup.addTab(tabontif.TabNotification(self.tray), self.tabsTitle[2])

        vLayout.addLayout(self.layoutSubTitle)
        vLayout.addWidget(self.tabGroup)

        # setting central widget
        mainVLayoutWidget = QWidget()
        mainVLayoutWidget.setLayout(vLayout)
        self.setCentralWidget(mainVLayoutWidget)

        self.show()

        # self.syncData()

    def closeEvent(self, event):
        event.accept()

    def syncData(self):
        sql = SQLAutoSync.SQLAutoSync()
        i = str(sql.getFirstInstallStatus())

        if i == '0':
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
        try:
            res_fb = f.getGymMetaData(ph)
            if res_fb == {}:
                self.forceLogOut()
        except Exception as e:
            print('Error : MainWindow().checkLastUserLoginStatus :: ' + str(e))

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
            MainWindowApplication(self.tray)
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

    # Custom notification
    def showCustomNotification(self, title, msg, time):
        if time == -1:
            self.tray.showMessage(
                title, msg, QIcon(cfg.TITLEBAR_ICON_URL)
            )
        else:
            self.tray.showMessage(
                title, msg, QIcon(cfg.TITLEBAR_ICON_URL),
                time
            )

    def showSplashScreen(self):
        splash_pix = QPixmap(cfg.SPLASH_SCREEN_URL)
        # splash_pix.scaled(400, 300) # Default - 800 * 600
        self.splash = QSplashScreen(splash_pix.scaled(800, 600), Qt.WindowStaysOnTopHint)
        self.splash.mousePressEvent = self.splashClicked
        # TODO : Uncomment this
        # self.splash.show()

    def splashClicked(self, e):
        self.splash.close()

    def forceLogOutToExtendMembership(self, days):
        m = CustomCriticalMessageBox()
        m.setWindowTitle('Alert!')
        msg = ''
        if days == 0:
            msg = 'Your membership will expire tomorrow. To continue using this application please ' \
                  'update payment with your vendor.'
            m.setText(msg)
            m.exec_()
        elif 1 <= days <= 5:
            msg = 'Your membership is about to expire in ' + str(days) + ' days. To continue using this application please ' \
                  'update payment with your vendor.'
            m.setText(msg)
            m.exec_()
        elif days < 0:
            msg = 'Your membership has expired please update vendor payment to continue using services.'
            m.setText(msg)
            reply = m.exec_()
            if reply == QMessageBox.Ok:
                self.close()


# LIVE MainWindow Thread SYSTEM
class ThreadLiveSoftwareDataControl(QThread):
    force_logout = pyqtSignal(int)

    def __init__(self, tray):
        super(ThreadLiveSoftwareDataControl, self).__init__()
        self.tray = tray

    def run(self):
        fb = FBTabHome
        sql = SQLTabHome.SQLTabHome()
        gymid = sql.getGymId()
        while True:
            if self.isConnectedToInternet() != 200:
                print('TabMain().Thread() - Not Connected to internet!')
                format = '%Y-%m-%d %H:%M:%S'
                d = sql.getSoftwareValidityDate()
                d = datetime.datetime.strptime(d + ' 00:00:01', format)

                n = str(datetime.date.today())
                currentTime = datetime.datetime.strptime(n + ' 00:00:01', format)
                diff = (d - currentTime).days
                self.force_logout.emit(int(diff))
                time.sleep(20 * 60)
                continue

            print('TabMain().Thread() - Connected to internet!')

            currentTime = sql.getSoftwareValidityDate()
            gymAdminAData = fb.getOnlineValidity(gymid)

            if str(currentTime) != str(gymAdminAData[cfg.FB_KEY_ADMIN_VALIDITY]):
                sql.updateSoftwareValidityDate(gymAdminAData[cfg.FB_KEY_ADMIN_VALIDITY])

            sql.updateCompleteAdminData(gymAdminAData)

            format = '%Y-%m-%d %H:%M:%S'
            d = sql.getSoftwareValidityDate()
            d = datetime.datetime.strptime(d + ' 00:00:01', format)

            n = str(datetime.date.today())
            currentTime = datetime.datetime.strptime(n + ' 00:00:01', format)
            diff = (d - currentTime).days
            self.force_logout.emit(int(diff))

            time.sleep(60 * 60)

    def convertToSQLDateFormat(self, s):
        inFormat = '%d %B, %Y'
        sqlFormat = '%Y-%m-%d'
        s = datetime.datetime.strptime(s, inFormat).strftime(sqlFormat)
        return s

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
