from PyQt5.QtCore import *
import accesscontrol.LoginScreenFB as loginfb
import accesscontrol.LoginScreenSQL as loginsql
from CustomMessageBox import *
import hashlib, os


class LoginScreen(QDialog):
    def __init__(self, atleastOneUserStatus):
        super(LoginScreen, self).__init__()
        self.loginStatus = -999
        self.correctCred = False
        self.atleastOneUserStatus = atleastOneUserStatus
        self.init(500, 300, 20)

    def init(self, winWidth, winHeight, winMargins):
        self.loginCount = 0
        self.setWindowTitle(cfg.APP_NAME)
        self.setMinimumSize(winWidth, winHeight)
        self.resize(winWidth, winHeight)

        self.vLayout = QVBoxLayout()
        self.vLayout.setSpacing(winMargins)
        # self.vLayout.setMargin(2 * winMargins)

        logo = QLabel(cfg.APP_NAME)
        logoPixmap = QPixmap('./src/icons/ic_logo_blue.png')
        logo.setPixmap(logoPixmap.scaled(120, 80, Qt.KeepAspectRatio))

        idLabel = QLabel('Phone')
        passLabel = QLabel('Password')
        lblGymId = QLabel('Gym ID')
        self.comboGymIds = QComboBox()

        self.idField = QLineEdit()

        self.passField = QLineEdit()
        self.passField.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton('Login')
        self.loginButton.setDefault(True)
        self.loginButton.setAutoDefault(True)

        cancelButton = QPushButton('Cancel')
        cancelButton.setDefault(False)
        cancelButton.setAutoDefault(True)

        self.contactAdmin = QPushButton("Forgot Password...")

        grid = QGridLayout()

        grid.setSpacing(winMargins)

        grid.addWidget(idLabel, 1, 0)
        grid.addWidget(self.idField, 1, 1)
        grid.addWidget(passLabel, 2, 0)
        grid.addWidget(self.passField, 2, 1)
        grid.addWidget(lblGymId, 3, 0)
        grid.addWidget(self.comboGymIds, 3, 1)

        self.buttonGroup = QHBoxLayout()
        self.buttonGroup.setSpacing(winMargins)
        self.buttonGroup.addStretch(1)
        self.buttonGroup.addWidget(cancelButton)
        self.buttonGroup.addWidget(self.loginButton)

        logoLayout = QHBoxLayout()
        logoLayout.addStretch(1)
        logoLayout.addWidget(logo)
        logoLayout.addStretch(1)

        self.vLayout.addStretch(1)
        self.vLayout.addLayout(logoLayout)
        self.vLayout.addStretch(1)
        self.vLayout.addLayout(grid)
        self.vLayout.addStretch(1)
        self.vLayout.addLayout(self.buttonGroup)
        self.vLayout.addStretch(1)

        self.forgotPassword = QPushButton("Forgot Password...")
        self.forgotPassword.setMaximumWidth(150)
        self.forgotPassword.setMinimumWidth(150)
        # self.forgotPassword.setStyleSheet("color: red")
        self.buttonGroup.addWidget(self.forgotPassword)

        # Listener
        self.loginButton.clicked.connect(self.loginClick)
        cancelButton.clicked.connect(self.cancelClick)
        # self.forgotPassword.clicked.connect(self.forgotPasswordFunc)
        self.setLayout(self.vLayout)
        self.show()
        if self.atleastOneUserStatus:
            loginnSQL = loginsql.SQLUserAdmin()
            data = (loginnSQL.getGymID())
            self.comboGymIds.clear()
            self.comboGymIds.addItem(data)
            self.comboGymIds.setEditable(False)
        else:
            self.fillComboBox()

        #todo : delete later
        self.idField.setText("9876543210")
        self.passField.setText("1234")
        self.comboGymIds.setCurrentIndex(1)

    def fillComboBox(self):
        self.comboGymIds.clear()
        login = loginfb.LoginScreenFB()
        data = login.getGymIds()
        self.comboGymIds.addItems(data)

    def cancelClick(self):
        self.loginStatus = -1000
        self.close()

    def closeEvent(self, event):
        if self.correctCred:
            self.loginStatus = 1
        else:
            self.loginStatus = - 1000
        event.accept()

    def loginClick(self):
        phone = "+91" + self.idField.text().__str__().strip(" ")
        passwd = self.passField.text().__str__().strip(" ")

        s = loginsql.SQLUserAdmin()
        res = s.getLoginStatus(phone)

        f = loginfb.LoginScreenFB()
        res_fb = f.getGymMetaData(phone)

        if res == -1 and res_fb == {}:
            msg1 = CustomCriticalMessageBox()
            msg1.setWindowTitle("Alert!")
            msg1.setText("It seems your status has been blocked. Please speak to your vendor for further information.")
            msg1.exec_()
            return
        elif res == 0 and res_fb != {}:
            s.updateAdminLoginStatus(0)

        self.loginStatus = -999
        if self.atleastOneUserStatus == 1:
            print("firebaseLoginCheck() :: SQL DB...")
            myhash = hashlib.sha1(passwd.encode('utf-8'))
            loginnSQL = loginsql.SQLUserAdmin()
            data = loginnSQL.getAdminPasswd(phone)
            if data is None:
                msg = CustomCriticalMessageBox()
                msg.setWindowTitle("Wrong")
                msg.setText("The password you have entered is wrong. Please check the information you have entered "
                            "and try again!")
                msg.exec_()
                return
            else:
                if data[0] != 'abc':
                    if data[0] != myhash.hexdigest():
                        msg = CustomCriticalMessageBox()
                        msg.setWindowTitle("Wrong")
                        msg.setText("The password you have entered is wrong. Please check the information "
                                    "you have entered "
                                    "and try again!")
                        msg.exec_()
                    else:
                        self.correctCred = True
                        sql = loginsql.SQLUserAdmin()
                        sql.updateAdminLoginStatus(1)
                        self.updateCurrentUserLoggedInPhone(phone)
                        self.close()
                else:
                    self.firebaseLoginCheck(phone, passwd, res_fb)
        else:
            self.firebaseLoginCheck(phone, passwd, res_fb)

    def firebaseLoginCheck(self, phone, passwd, data):
        print("firebaseLoginCheck() :: Firebase DB...")
        loginFB = loginfb.LoginScreenFB()
        # data = loginFB.getGymMetaData(phone)
        if data == {} or data['passwd'] != passwd:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Wrong")
            msg.setText("The Information you have entered is wrong. Please check the information you have entered "
                        "and try again!")
            msg.exec_()
        else:
            self.correctCred = True
            sql = loginsql.SQLUserAdmin()
            sql.insertAdminData(data)
            sql.updateAdminLoginStatus(1)
            self.updateCurrentUserLoggedInPhone(phone)
            self.close()

    def updateCurrentUserLoggedInPhone(self, phone):
        if not os.path.exists(cfg.TMP_FILE_URL):
            f = open(cfg.TMP_FILE_URL, "w")
            f.close()

        f = open(cfg.TMP_FILE_URL, "w")
        f.write(phone)
        f.close()
