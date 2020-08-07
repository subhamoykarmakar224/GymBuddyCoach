from PyQt4.QtCore import *
import accesscontrol.LoginScreenFB as loginfb
import accesscontrol.LoginScreenSQL as loginsql
from CustomMessageBox import *


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.loginStatus = -999
        self.correctCred = False
        self.init(500, 300, 20)

    def init(self, winWidth, winHeight, winMargins):
        self.loginCount = 0
        self.setWindowTitle(cfg.APP_NAME)
        self.setMinimumSize(winWidth, winHeight)
        self.resize(winWidth, winHeight)

        self.vLayout = QVBoxLayout()
        self.vLayout.setSpacing(winMargins)
        self.vLayout.setMargin(2 * winMargins)

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
        self.fillComboBox()

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
        phone = "+91" + self.idField.text().__str__()
        passwd = self.passField.text().__str__()
        self.loginStatus = -999
        login = loginfb.LoginScreenFB()
        data = login.getGymMetaData(phone)
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
            self.close()
