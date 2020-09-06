from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime, time, requests

import Configuration as cfg
import home.SQLTabHome as SQLTabHome
import home.FBTabHome as FBTabHome
import home.CustomMessageMgmt as CustomMessageMgmt


class TabHome(QWidget):
    def __init__(self, tray):
        super(TabHome, self).__init__()
        self.tray = tray
        self.threadHome = ThreadLiveHomeTabControl(self.tray)
        self.threadHome.update_meta_data.connect(self.updateMetaDataDisplay)
        self.threadHome.start()

        adminPhoneNo = ""
        l = []
        with open(cfg.TMP_FILE_URL, "r") as f:
            l = f.readlines()

        adminPhoneNo = l[0].strip("\n").replace("\r", "")
        self.adminMetaData = {}
        sql = SQLTabHome.SQLTabHome()
        self.adminMetaData = sql.getGymAdminInfo(adminPhoneNo)

        # Layouts
        self.grid = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.subGrid = QGridLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblGymIDLabel = QLabel("Gym ID")
        self.lblQrCode = QLabel("QR Code")
        self.lblGymId = QLabel(self.adminMetaData[cfg.KEY_ADMIN_ID])
        self.lblGymName = QLabel(self.adminMetaData[cfg.KEY_ADMIN_GYM_NAME])
        self.lblAdminName = QLabel(self.adminMetaData[cfg.KEY_ADMIN_NAME])
        self.lblAdminUsername = QLabel(self.adminMetaData[cfg.KEY_ADMIN_USERNAME])
        self.lblAdminPhone = QLabel(self.adminMetaData[cfg.KEY_ADMIN_PHONE])
        self.lblAdminValidity = QLabel(
            self.convertSQLDateFormatToCustom(
                self.adminMetaData[cfg.KEY_ADMIN_VALIDITY]
            ))
        self.groupBoxGymMetaInformation = QGroupBox("Gym Information")
        self.groupBoxCustomMsg = QGroupBox("Custom Message Management")

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.subGrid.addWidget(self.lblGymIDLabel, 0, 0)
        self.subGrid.addWidget(self.lblGymId, 0, 1)
        self.subGrid.addWidget(self.lblQrCode, 0, 2, 6, 1)
        self.subGrid.addWidget(QLabel('Gym Name'), 1, 0)
        self.subGrid.addWidget(self.lblGymName, 1, 1)
        self.subGrid.addWidget(QLabel('Admin Name'), 2, 0)
        self.subGrid.addWidget(self.lblAdminName, 2, 1)
        self.subGrid.addWidget(QLabel('Username'), 3, 0)
        self.subGrid.addWidget(self.lblAdminUsername, 3, 1)
        self.subGrid.addWidget(QLabel('Phone'), 4, 0)
        self.subGrid.addWidget(self.lblAdminPhone, 4, 1)
        self.subGrid.addWidget(QLabel('Software Validity'), 5, 0)
        self.subGrid.addWidget(self.lblAdminValidity, 5, 1)

        # Add to Group Box
        self.groupBoxGymMetaInformation.setLayout(self.subGrid)
        self.groupBoxCustomMsg.setLayout(CustomMessageMgmt.CustomMessageMgmt())

        # Add to Main Layout
        self.grid.addWidget(self.groupBoxGymMetaInformation, 0, 0)
        self.grid.addWidget(self.groupBoxCustomMsg, 1, 0)

        # Add Main Widget to Parent Layout
        self.setLayout(self.grid)

    def setLayoutProperties(self):
        self.grid.setAlignment(Qt.AlignTop)

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        self.lblGymIDLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lblGymIDLabel.setFixedWidth(120)
        qrCodePixmap = QPixmap(cfg.QR_CODE_URL)
        self.lblQrCode.setPixmap(
            qrCodePixmap.scaled(
                150, 150,
                Qt.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation)
        )
        self.lblQrCode.setAlignment(Qt.AlignRight)

    def setListeners(self):
            pass

    def convertSQLDateFormatToCustom(self, s):
        s = str(s).split("-")
        m = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }
        return s[0] + " " + m[s[1]] + ", " + s[2]

    def updateMetaDataDisplay(self, f):
        sql = SQLTabHome.SQLTabHome()
        if f:
            with open(cfg.TMP_FILE_URL, "r") as f:
                l = f.readlines()

            adminPhoneNo = l[0].strip("\n").replace("\r", "")
            data = sql.getGymAdminInfo(adminPhoneNo)
            # {'gymId': 'BodyShapersGym-2932', 'gymName': 'Body Shapers Gym', 'adminName': 'Modi',
            #  'phone': '+919876543219', 'validity': '2020-09-10', 'username': 'mods'}
            self.lblGymName.setText(data['gymName'])
            self.lblAdminName.setText(data['adminName'])
            self.lblAdminPhone.setText(data['phone'])
            self.lblAdminValidity.setText( self.convertSQLDateFormatToCustom(
                data['validity']
            ))

        del sql


# LIVE MainWindow Thread SYSTEM
class ThreadLiveHomeTabControl(QThread):
    update_meta_data = pyqtSignal(bool)

    def __init__(self, tray):
        super(ThreadLiveHomeTabControl, self).__init__()
        self.tray = tray

    def run(self):
        while True:
            if self.isConnectedToInternet() != 200:
                continue

            # print('TabHome().Thread() - Connected to internet!')

            self.update_meta_data.emit(True)

            time.sleep(2)

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
