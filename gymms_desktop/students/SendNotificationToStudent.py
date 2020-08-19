from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, os, datetime

from Helper import *
from CustomMessageBox import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents


class SendNotificationToStudent(QDialog):
    def __init__(self, data):
        super(SendNotificationToStudent, self).__init__()

        # [ ('ID-2932-5d8d6b34', 'Test 1 '),
        # ('ID-2932-7e24dabd', 'Subhamoy Karmakar'),
        # ('ID-2932-da96eb71', 'Elon TRON Musk') ]
        self.data = data
        self.allOkStatus = False
        self.setWindowTitle(cfg.APP_NAME + " : Send Notification")
        self.setFixedWidth(800)
        self.setFixedHeight(520)
        self.setContentsMargins(20, 20, 20, 20)

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutButtons = QHBoxLayout()
        self.layoutProgress = QHBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.table = QTableWidget()
        self.lblCounter = QLabel('300 left')
        self.messageTextArea = QTextEdit()
        self.btnSend = QPushButton('Send')
        self.btnCancel = QPushButton('Cancel')
        self.btnLoadMsgTemplate = QPushButton('Load From Template')
        self.lblProgress = QLabel("0% Done")
        self.progressBar = QProgressBar()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutButtons.addWidget(self.btnSend)
        self.layoutButtons.addWidget(self.btnCancel)
        self.layoutButtons.addWidget(self.btnLoadMsgTemplate)
        self.layoutProgress.addWidget(self.lblProgress)
        self.layoutProgress.addWidget(self.progressBar)

        # Add to Main Layout
        self.mainLayout.addWidget(QLabel("Members"), 0, 0)
        self.mainLayout.addWidget(self.table, 1, 0)
        self.mainLayout.addWidget(QLabel("Message (Max of 300 characters)"), 0, 1)
        self.mainLayout.addWidget(self.lblCounter, 0, 2)
        self.mainLayout.addWidget(self.messageTextArea, 1, 1, 1, 2)
        self.mainLayout.addLayout(self.layoutButtons, 2, 1)
        self.mainLayout.addLayout(self.layoutProgress, 2, 0)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

        self.refreshTable()

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        self.layoutButtons.setStretch(2, 1)

    def setWidgetProperties(self):
        self.lblCounter.setAlignment(Qt.AlignRight)
        self.messageTextArea.setPlaceholderText("Your message here...")
        self.columnsHeaders = ['ID', 'Name', '']
        self.table.setColumnCount(self.columnsHeaders.__len__())
        self.table.setHorizontalHeaderLabels(self.columnsHeaders)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 20)

    def setListeners(self):
        self.table.cellClicked.connect(self.removeStudentDataFromTable)
        self.messageTextArea.textChanged.connect(self.wordCounter)
        self.btnCancel.clicked.connect(self.closeMessage)
        self.btnSend.clicked.connect(self.sendMessage)

    def refreshTable(self):
        self.table.clearContents()
        self.table.setRowCount(len(self.data))
        for i in range(len(self.data)):
            self.table.setItem(i, 0, QTableWidgetItem(self.data[i][0]))
            self.table.setItem(i, 1, QTableWidgetItem(self.data[i][1]))
            btnDelete = QLabel()
            btnDelete.setPixmap(getPixMap(cfg.IC_DELETE_COLOR))
            btnDelete.setCursor(Qt.PointingHandCursor)
            self.table.setCellWidget(i, 2, btnDelete)

    # Get student IDs of checked rows
    def removeStudentDataFromTable(self, r, c):
        if c != 2:
            return

        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Alert")
        msg.setText("Are you sure you don't want to send notification to the selected student?")
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.No:
            return

        deleteId = self.table.item(r, 0).text()
        for i in range(len(self.data)):
            if self.data[i][0] == deleteId:
                self.data.pop(i)
                break

        if len(self.data) == 0:
            self.allOkStatus = True
            self.close()

        self.refreshTable()

    def wordCounter(self):
        cnt = 300 - self.messageTextArea.toPlainText().__str__().__len__() + 1
        if cnt == 0:
            tmp = self.messageTextArea.toPlainText().__str__()
            tmp = tmp[:len(tmp)-1]
            self.messageTextArea.setPlainText(tmp)
            self.messageTextArea.moveCursor(QTextCursor.End)
        elif cnt == 299:
            self.lblCounter.setText("300 left")
        else:
            self.lblCounter.setText(str(cnt-1) + ' left')

    def closeMessage(self):
        self.close()

    # Checks if the user presses cancel button
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.closeMessage()

    # Triggers on close window event
    def closeEvent(self, event):
        if self.allOkStatus:
            event.accept()
            return

        msg = CustomCriticalMessageBox()
        msg.setWindowTitle("Alert")
        msg.setText('Any unsaved changes will be lost. Are you sure you want to continue? ')
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def sendMessage(self):
        sql = SQLTabStudents.SQLTabStudents()
        gymid = sql.getGymId()
        msg = self.messageTextArea.toPlainText().__str__()
        # [('ID-2932-5d8d6b34', 'Test 1 '),
        # ('ID-2932-7e24dabd', 'Subhamoy Karmakar'),
        # ('ID-2932-da96eb71', 'Elon TRON Musk')]
        # Hello!
        sids = []
        for sid in self.data:
            sids.append(sid)
        lastIndexVal = sql.getLastNotificationMsgCnt()[0]
        lastIndexVal = lastIndexVal + 1
        res = 100 / len(self.data)
        inBetweenConnBreak = False
        for i in range(len(self.data)):
            res = res + (i*res)
            print("Done : ", res)
            self.lblProgress.setText(str(int(res)) + "% Done")
            self.progressBar.setValue(int(res))
            if self.isConnectedToInternet() == 200:
                FBTabStudents.sendNotification(lastIndexVal, sids[i], msg, gymid)
                lastIndexVal += 1
            else:
                inBetweenConnBreak = True

        if not inBetweenConnBreak:
            self.progressBar.setValue(100)
            sql.sendNotificationsMsg(sids, msg)
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Notification sent to all students.")
            msg.exec_()
            self.allOkStatus = True
            self.close()
        else:
            msg = CustomCriticalMessageBox()
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Failure")
            msg.setText("Please check your internet connection and try again.")
            msg.exec_()



    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
