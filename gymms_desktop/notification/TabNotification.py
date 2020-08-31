from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time, requests

import Configuration as cfg
from notification import FBTabNotification
from notification.FBTabNotification import *
import notification.SQLTabNotification as SQLTabNotification


class TabNotification(QWidget):
    def __init__(self, tray):
        super(TabNotification, self).__init__()

        self.tray = tray

        # Layouts
        self.layout = QGridLayout()
        self.calender = QDateEdit(calendarPopup=True)

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutBtn = QHBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.table = QTableWidget()
        self.startTimePicker = QTimeEdit()
        self.endTimePicker = QTimeEdit()
        self.editTextSearchTerm = QPlainTextEdit()
        self.comboLevels = QComboBox()
        self.btnSearch = QPushButton("Filter")
        self.btnReset = QPushButton("Reset")

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutBtn.addWidget(self.btnSearch)
        self.layoutBtn.addWidget(self.btnReset)

        # Add to Main Layout
        self.layout.addWidget(QLabel('Notification'), 0, 0)
        self.layout.addWidget(self.table, 1, 0, 11, 1)
        self.layout.addWidget(QLabel('Filter'), 0, 1)
        self.layout.addWidget(QLabel('Calender'), 1, 1)
        self.layout.addWidget(self.calender, 2, 1)
        self.layout.addWidget(QLabel("From"), 3, 1)
        self.layout.addWidget(self.startTimePicker, 4, 1)
        self.layout.addWidget(QLabel("To"), 5, 1)
        self.layout.addWidget(self.endTimePicker, 6, 1)
        self.layout.addWidget(QLabel("Levels"), 7, 1)
        self.layout.addWidget(self.comboLevels, 8, 1)
        self.layout.addWidget(QLabel("Search"), 9, 1)
        self.layout.addWidget(self.editTextSearchTerm, 10, 1)
        self.layout.addLayout(self.layoutBtn, 11, 1)

        # self.layout.addLayout(self.layoutCalenderOptions, 1, 1)

        # Add Main Widget to Parent Layout
        self.setLayout(self.layout)

        self.refreshNotificationTable('')
        self.startNotificationBackgroundProcess()

    def setLayoutProperties(self):
        self.layout.setAlignment(Qt.AlignTop)

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        self.columnsHeaders = ['Date', 'Time', 'Level', 'Student ID', 'Student Name', 'Message']
        self.table.setColumnCount(self.columnsHeaders.__len__())
        self.table.setHorizontalHeaderLabels(self.columnsHeaders)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 200)
        # self.table.cellDoubleClicked.connect(self.onCellDoubleClickAction)

        self.calender.setDisplayFormat("dd MMMM, yyyy")
        self.calender.setDate(QDate.currentDate())

        self.startTimePicker.setTime(QTime(0, 0))
        self.endTimePicker.setTime(QTime(23, 59))

        self.comboLevels.addItems(["All", "Green", "Red"])
        self.comboLevels.setCurrentIndex(0)

        self.editTextSearchTerm.setPlaceholderText("Your search term here...")
        self.editTextSearchTerm.setFixedWidth(300)

    def setListeners(self):
        self.calender.dateChanged.connect(self.dateChangedEvent)
        self.btnSearch.clicked.connect(self.filterData)
        self.btnReset.clicked.connect(self.resetAll)

    def refreshNotificationTable(self, d):
        sql = SQLTabNotification.SQLTabNotification()
        notifs = sql.getAllNotificationsFromToday(d)
        self.table.clearContents()
        self.table.setRowCount(len(notifs))
        self.fillTable(notifs)
        del sql

    # Tue Aug 04 19:16:38 GMT+05:30 2020
    def convertToCustomDateTimeFormat(self, d):
        resDate = ''
        d = d.split(" ")
        months = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        resDate = d[2] + "-" + months[d[1]] + "-" + d[-1]
        return resDate, d[3]

    # Reset the whole view
    def resetAll(self):
        self.calender.setDate(QDate.currentDate())
        self.startTimePicker.setTime(QTime(0, 0))
        self.endTimePicker.setTime(QTime(23, 59))
        self.comboLevels.setCurrentIndex(0)
        self.editTextSearchTerm.setPlainText('')
        self.refreshNotificationTable('')

    def dateChangedEvent(self, e):
        self.startTimePicker.setTime(QTime(0, 0))
        self.endTimePicker.setTime(QTime(23, 59))
        self.comboLevels.setCurrentIndex(0)

    # Custom local notification alart
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

    def refreshNotificationTable(self, d):
        sql = SQLTabNotification.SQLTabNotification()
        notifs = sql.getAllNotificationsFromToday(d)
        self.table.clearContents()
        self.table.setRowCount(len(notifs))
        self.fillTable(notifs)
        del sql

    # Filter Data as per input
    def filterData(self):
        d = self.calender.date().toString("dd-MM-yyyy")
        starttime = self.startTimePicker.time().toString("HH:mm")
        endtime = self.endTimePicker.time().toString('HH:mm')
        level = self.comboLevels.currentText()
        searchtext = self.editTextSearchTerm.toPlainText()
        data = (d, starttime, endtime, level, searchtext)
        sql = SQLTabNotification.SQLTabNotification()
        notifs = sql.getFilteredNotification(data)
        self.table.clearContents()
        self.table.setRowCount(len(notifs))
        self.fillTable(notifs)
        del sql

    # Fill Table
    def fillTable(self, notifs):
        sql = SQLTabNotification.SQLTabNotification()
        for i in range(len(notifs)):
            n = notifs[i]
            d, t = self.convertToCustomDateTimeFormat(n[2])
            self.table.setItem(i, 0, QTableWidgetItem(d))
            self.table.setItem(i, 1, QTableWidgetItem(t))
            self.table.setItem(i, 2, QTableWidgetItem(n[5]))
            self.table.setItem(i, 3, QTableWidgetItem(n[1]))
            self.table.setItem(i, 4, QTableWidgetItem(sql.getStudentName(n[1])))
            self.table.setItem(i, 5, QTableWidgetItem(n[-1]))

        del sql

    def startNotificationBackgroundProcess(self):
        self.thread = ThreadLiveNotificationShow(self.tray)
        self.thread.refresh_table.connect(self.refreshTableFromThread)
        self.thread.start()

    def refreshTableFromThread(self, v):
        self.btnSearch.click()


# LIVE NOTIFICATION SYSTEM
class ThreadLiveNotificationShow(QThread):
    refresh_table = pyqtSignal(bool)

    def __init__(self, tray):
        super(ThreadLiveNotificationShow, self).__init__()
        self.tray = tray

    def run(self):

        fb = FBTabNotification
        sql = SQLTabNotification.SQLTabNotification()
        gymid = sql.getGymId()
        while True:
            time.sleep(20)
            if self.isConnectedToInternet() != 200:
                print('TabNotification().Thread() - Not Connected to internet!')
                continue

            print('TabNotification().Thread() - Connected to internet!')

            sql.getAttendenceNotUploadedForUpload()
            sql.deleteNotificationOlderThan15Days()
            tmpSQLCount = sql.getAllNotificationCount()
            notificationS = fb.getAllNotification(gymid)
            if tmpSQLCount[0] == len(notificationS.keys()):
                continue

            for k in notificationS.keys():
                n = notificationS[k]
                tmpCnt = sql.getIsNotificationPresent(n[cfg.FB_KEY_NOTIFICATION_SID])
                if tmpCnt[0] <= 0:
                    sql.insertNotifications(k, n)
                    self.tray.showMessage(
                        "Notification!", n[cfg.FB_KEY_NOTIFICATION_SID] + "\n" +
                                         n[cfg.FB_KEY_NOTIFICATION_LEVEL] + "\n" + n[cfg.FB_KEY_NOTIFICATION_MSG],
                        QIcon(cfg.TITLEBAR_ICON_URL)
                    )
            self.refresh_table.emit(True)

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
