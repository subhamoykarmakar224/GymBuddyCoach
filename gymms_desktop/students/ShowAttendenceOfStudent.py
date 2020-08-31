from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import uuid, shutil, os, datetime, time, requests, calendar

import Configuration as cfg
from Helper import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents
from CustomMessageBox import *


class ShowAttendenceOfStudent(QDialog):
    def __init__(self, sid, name):
        super(ShowAttendenceOfStudent, self).__init__()
        self.setWindowTitle(cfg.APP_NAME + " : Attendance")
        self.sid = sid
        self.name = name

        self.months = {
            'January': '01','February': '02','March': '03','April': '04','May': '05','June': '06',
            'July': '07','August': '08','September': '09','October': '10','November': '11','December': '12'
        }

        self.setFixedWidth(400)
        self.setFixedHeight(440)

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutCal = QGridLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblTitle = QLabel(self.sid + " - " + self.name)
        self.lblTime = QLabel('-na-')
        self.comboMonths = QComboBox()
        self.comboYear = QComboBox()
        self.btnRefresh = QLabel()
        self.table = QTableWidget()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout

        # Add to Main Layout
        self.mainLayout.addWidget(self.lblTitle, 0, 0, 1, 4)
        self.mainLayout.addWidget(QLabel("Month"), 1, 0)
        self.mainLayout.addWidget(self.comboMonths, 1, 1)
        self.mainLayout.addWidget(QLabel("Time"), 1, 2)
        self.mainLayout.addWidget(self.lblTime, 1, 3)
        self.mainLayout.addWidget(QLabel('Year'), 2, 0)
        self.mainLayout.addWidget(self.comboYear, 2, 1)
        self.mainLayout.addWidget(self.btnRefresh, 2, 2)
        self.mainLayout.addWidget(self.table, 3, 0, 1, 5)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

        self.generateCalender()

    def setLayoutProperties(self):
        self.mainLayout.setAlignment(Qt.AlignTop)

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        self.comboMonths.clear()
        self.comboMonths.addItems(self.months.keys())
        m = datetime.datetime.now().month
        self.comboMonths.setCurrentIndex(m-1)

        self.comboYear.clear()
        s = 1990
        e = datetime.datetime.now().year
        self.comboYear.addItems([str(i) for i in range(e, s, -1)])

        self.btnRefresh.setPixmap(getPixMap(cfg.IC_REFRESH_COLOR))
        self.btnRefresh.setCursor(Qt.PointingHandCursor)
        self.btnRefresh.setToolTip("Refresh")
        self.btnRefresh.setAlignment(Qt.AlignTop)

        columnsHeaders = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.table.setColumnCount(columnsHeaders.__len__())
        self.table.setHorizontalHeaderLabels(columnsHeaders)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setFixedWidth(380)
        self.table.setFixedHeight(335)
        wid = 53
        self.table.setColumnWidth(0, wid)
        self.table.setColumnWidth(1, wid)
        self.table.setColumnWidth(2, wid)
        self.table.setColumnWidth(3, wid)
        self.table.setColumnWidth(4, wid)
        self.table.setColumnWidth(5, wid)
        self.table.setColumnWidth(6, wid)
        self.table.setRowCount(6)
        header = self.table.verticalHeader()
        header.setDefaultSectionSize(50)
        header.sectionResizeMode(QHeaderView.Fixed)
        header.setVisible(False)

    def setListeners(self):
        self.comboMonths.currentIndexChanged.connect(self.generateCalender)
        self.comboYear.currentIndexChanged.connect(self.generateCalender)
        self.table.cellClicked.connect(self.populateTime)
        self.btnRefresh.mousePressEvent = self.btnRefreshMonthYear

    def generateCalender(self):
        for i in range(0, 8):
            for j in range(0, 7):
                self.table.setItem(i, j, QTableWidgetItem(''))
        self.lblTime.setText('-na-')
        m = self.months[self.comboMonths.currentText()]
        y = self.comboYear.currentText()
        endCounter = calendar.monthrange(int(y), int(m))[1]
        startDayofweek = datetime.date(int(y), int(m), 1).weekday()
        dayCounter = 1
        row = 0
        col = startDayofweek
        sql = SQLTabStudents.SQLTabStudents()
        data = sql.getAttendanceForAMonth(self.sid, str(m), str(y), str(endCounter))
        del sql

        self.green_dates = {}

        for d in data:
            tmp = str(d[1]).split('-')
            self.green_dates[int(tmp[2])] = str(d[2])

        while True:
            if self.green_dates.keys().__contains__(dayCounter):
                self.table.setItem(row, col, QTableWidgetItem(str(dayCounter)))
                self.table.item(row, col).setBackground(QColor(46, 125, 50))
            else:
                self.table.setItem(row, col, QTableWidgetItem(str(dayCounter)))

            if dayCounter == endCounter:
                break

            dayCounter += 1
            col += 1
            if col == 7:
                col = 0
                row += 1

    def populateTime(self, r, c):
        d = self.table.item(r, c).text()
        if d == '':
            self.lblTime.setText('-na-')
            return

        if not self.green_dates.keys().__contains__(int(d)):
            self.lblTime.setText('-na-')
        elif self.green_dates.keys().__contains__(int(d)):
            t = self.green_dates[int(d)]
            t = time.strptime(t, "%H:%M:%S")
            t = time.strftime("%I:%M %p", t)
            self.lblTime.setText(str(t))

    def btnRefreshMonthYear(self, e):
        m = datetime.datetime.now().month
        self.comboMonths.setCurrentIndex(m - 1)
        self.comboYear.setCurrentIndex(0)
