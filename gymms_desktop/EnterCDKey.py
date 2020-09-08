from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from uuid import getnode
import pyrebase, requests
import mysql.connector as mysql

import Configuration as cfg


class EnterCDKey(QDialog):
    def __init__(self):
        super(EnterCDKey, self).__init__()
        self.allOK = False
        self.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        self.setWindowTitle('Gym Management System')
        self.MAC = getnode()
        self.setFixedWidth(400)
        self.setFixedHeight(150)

        self.FB_TABLE_CDKEY = 'CD_KEY'
        self.KEY_CDKEY_NAME = 'NAME'
        self.KEY_CDKEY_PHONE = 'PHONE'
        self.KEY_CDKEY_MAC = 'MAC'
        self.KEY_CDKEY_KEY = 'KEY'

        grid = QGridLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText('Your name here.')
        self.phone = QLineEdit()
        self.phone.setPlaceholderText('Your registered phone number with out STD code.')
        self.cdkey = QLineEdit()
        self.cdkey.setPlaceholderText('You CD key you got from vendor.')
        self.btnRegister = QPushButton('Register')
        self.btnRegister.setCursor(Qt.PointingHandCursor)

        grid.setAlignment(Qt.AlignTop)

        grid.addWidget(QLabel('Name'), 0, 0)
        grid.addWidget(self.name, 0, 1)
        grid.addWidget(QLabel('Phone'), 1, 0)
        grid.addWidget(self.phone, 1, 1)
        grid.addWidget(QLabel('CD-KEY'), 2, 0)
        grid.addWidget(self.cdkey, 3, 0, 1, 2)
        grid.addWidget(self.btnRegister, 4, 0, 1, 2)

        self.btnRegister.clicked.connect(self.btnRegisterClicked)

        self.setLayout(grid)

        if self.isConnectedToInternet() != 200:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
            msg.setWindowTitle('Critical')
            msg.setIcon(QMessageBox.Critical)
            msg.setText('You need to be connected to the internet to continue.')
            r = msg.exec_()
            if r == QMessageBox.Ok:
                self.close()

    def btnRegisterClicked(self):
        name = self.name.text()
        phone = self.phone.text()
        key = self.cdkey.text()

        valid = True

        if len(name) == 0:
            valid = False

        if valid and (len(phone) == 0 or len(phone) != 10):
            valid = False

        key = key.replace('-', '').lower()

        if valid and (len(key) == 0 or len(key) < 20):
            valid = False

        if not valid:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
            msg.setWindowTitle('Error')
            msg.setText('Invalid fields. Please check the fields and try again')
            msg.exec_()
        else: # e9c3-ae07-a929-49ce-85fb
            adminData = self.getGymMetaData(phone)

            if adminData == {}:
                msg = QMessageBox()
                msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
                msg.setWindowTitle('Critical')
                msg.setIcon(QMessageBox.Critical)
                msg.setText('The phone number you have entered is not present in our database. Please check the number '
                            'and try again.')
                msg.exec_()
                return

            if adminData.keys().__contains__('MAC'):
                if adminData['MAC'] != self.MAC:
                    msg = QMessageBox()
                    msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
                    msg.setWindowTitle('Critical')
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText('The Key you have entered is already in use. Please contact admin to get a new key.')
                    r = msg.exec_()
                    if r == QMessageBox.Ok:
                        self.close()

            if adminData['cdkey'] == key:
                self.allOK = True
                self.updateGymMACAddress(adminData['gymId'])
                self.insertCDKey(key)
                msg = QMessageBox()
                msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
                msg.setWindowTitle('Success')
                msg.setIcon(QMessageBox.Information)
                msg.setText('Congratulations! Please keep you CD Key safe.')
                r = msg.exec_()
                if r == QMessageBox.Ok:
                    self.close()
            else:
                msg = QMessageBox()
                msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
                msg.setWindowTitle('Critical')
                msg.setIcon(QMessageBox.Critical)
                msg.setText('The Key you have entered does not match with our database.')
                msg.exec_()

    def getGymMetaData(self, phone):
        phone = '+91' + phone
        db = self.getFirebaseDBObject()

        res = db.child(cfg.FB_TABLE_ADMIN) \
            .order_by_child(cfg.FB_KEY_ADMIN_PHONE) \
            .equal_to(phone).get()
        data = {}
        if res.each().__len__() == 0:
            data = {}
        else:
            for r in res.each():
                data = r.val()
        del db
        return data

    def updateGymMACAddress(self, gymId):
        db = self.getFirebaseDBObject()
        # db.child(cfg.FB_TABLE_ADMIN).child(gymId).child('MAC').update(self.MAC)
        db.child(cfg.FB_TABLE_ADMIN) \
            .child(gymId) \
            .update({"MAC": self.MAC})
        del db

    def getFirebaseDBObject(self):
        firebase = pyrebase.initialize_app(cfg.FB_CONFIG)
        return firebase.database()

    def insertCDKey(self, key):
        db = mysql.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            passwd=cfg.db_passwd,
            db=cfg.db_gymms
        )
        cur = db.cursor()
        query = 'insert into ' + cfg.TABLE_CDKEY + ' values("' + key + '")'
        try:
            cur.execute(query)
            db.commit()
        except Exception as e:
            print("EnterCDKey.insertCDKey() :: ERROR :: " + str(e))

        del cur
        del db

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
