from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import Dashboard as dash


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.initUI(500, 300, 20)

    def initUI(self, winWidth, winHeight, winMargins):
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

        # self.forgotPassword = QPushButton("Forgot Password...")
        # self.forgotPassword.setMaximumWidth(150)
        # self.forgotPassword.setMinimumWidth(150)
        # self.forgotPassword.setStyleSheet("color: red")
        # self.buttonGroup.addWidget(self.forgotPassword)

        # Listener
        self.loginButton.clicked.connect(self.loginClick)
        cancelButton.clicked.connect(self.cancelClick)
        # self.forgotPassword.clicked.connect(self.forgotPasswordFunc)

        self.setLayout(self.vLayout)
        self.show()

    def cancelClick(self):
        self.close()

    def loginClick(self):
        # self.close()
        dash.Dashboard("9878766554")