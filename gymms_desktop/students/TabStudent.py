from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests

import Configuration as cfg
from Helper import *
from CustomMessageBox import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents
import students.StudentDetails as StudentDetails


class TabStudent(QWidget):
    def __init__(self):
        super(TabStudent, self).__init__()

        self.selectedStudent = []

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutSearch = QHBoxLayout()
        self.layoutButtons = QVBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblStudents = QLabel("Students List")
        self.lineEdtSearch = QLineEdit()
        self.lblClearIcon = QLabel()
        self.pixMapICClear = QPixmap(cfg.IC_DELETE)
        self.table = QTableWidget()
        self.btnNewStudents = QLabel()
        self.btnEditStudents = QLabel()
        self.btnSubscription = QLabel()
        self.btnDeleteStudents = QLabel()
        self.btnSendNotifStudents = QLabel()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutSearch.addWidget(self.lineEdtSearch)
        self.layoutSearch.addWidget(self.lblClearIcon)

        self.layoutButtons.addWidget(self.btnNewStudents)
        self.layoutButtons.addWidget(self.btnEditStudents)
        self.layoutButtons.addWidget(self.btnSubscription)
        self.layoutButtons.addWidget(self.btnSendNotifStudents)
        self.layoutButtons.addWidget(self.btnDeleteStudents)

        # Add to Main Layout
        self.mainLayout.addWidget(self.lblStudents, 0, 0, 1, 2)
        self.mainLayout.addLayout(self.layoutSearch, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.table, 2, 0)
        self.mainLayout.addLayout(self.layoutButtons, 2, 3)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

        # self.refreshStudentsTable()

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        self.layoutButtons.addStretch(0)

    def setWidgetProperties(self):
        # Search LineEdit
        self.lineEdtSearch.setPlaceholderText("Search...")
        self.lblClearIcon.setPixmap(self.pixMapICClear.scaled(15, 15, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.lblClearIcon.setCursor(Qt.PointingHandCursor)
        self.lblClearIcon.setToolTip("Clear Search Term")

        # Student List table
        self.columnsHeaders = ['#', 'ID', 'Name', 'Alloted Time', 'Membership Validity', 'Due Amount']
        self.table.setColumnCount(self.columnsHeaders.__len__())
        self.table.setHorizontalHeaderLabels(self.columnsHeaders)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnWidth(0, 20)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 300)
        self.table.setColumnWidth(4, 200)
        self.table.cellDoubleClicked.connect(self.onCellDoubleClickAction)

        # Btn new students
        self.btnNewStudents.setPixmap(getPixMap(cfg.IC_ADD))
        self.btnNewStudents.setCursor(Qt.PointingHandCursor)
        self.btnNewStudents.setToolTip("Add new students")
        self.btnNewStudents.setAlignment(Qt.AlignTop)

        self.btnEditStudents.setPixmap(getPixMap(cfg.IC_EDIT))
        self.btnEditStudents.setCursor(Qt.PointingHandCursor)
        self.btnEditStudents.setToolTip("Edit Selected Student")
        self.btnEditStudents.setAlignment(Qt.AlignTop)

        self.btnSubscription.setPixmap(getPixMap(cfg.IC_SUBSCRIPTION))
        self.btnSubscription.setCursor(Qt.PointingHandCursor)
        self.btnSubscription.setToolTip("Extend Subscription")
        self.btnSubscription.setAlignment(Qt.AlignTop)

        self.btnDeleteStudents.setPixmap(getPixMap(cfg.IC_TRASH))
        self.btnDeleteStudents.setCursor(Qt.PointingHandCursor)
        self.btnDeleteStudents.setToolTip("Delete Student")
        self.btnDeleteStudents.setAlignment(Qt.AlignTop)

        self.btnSendNotifStudents.setPixmap(getPixMap(cfg.IC_MESSAGE))
        self.btnSendNotifStudents.setCursor(Qt.PointingHandCursor)
        self.btnSendNotifStudents.setToolTip("Send Notification")
        self.btnSendNotifStudents.setAlignment(Qt.AlignTop)

        # Refresh students table
        self.refreshStudentsTable()

    def setListeners(self):
        self.btnNewStudents.mousePressEvent = self.AddNewStudent
        self.btnEditStudents.mousePressEvent = self.EditStudent
        self.btnSubscription.mousePressEvent = self.EditSubscription
        self.btnDeleteStudents.mousePressEvent = self.DeleteStudent
        self.btnSendNotifStudents.mousePressEvent = self.SendNotificationToStudent

    def refreshStudentsTable(self):
        print("Load Table...")
        sqllocal = SQLTabStudents.SQLTabStudents()
        students = sqllocal.getAllStudents()
        self.table.clearContents()
        self.table.setRowCount(len(students))
        for i in range(len(students)):
            checkBox = QCheckBox()
            self.table.setCellWidget(i, 0, checkBox)
            self.table.setItem(i, 1, QTableWidgetItem(students[i][0]))
            self.table.setItem(i, 2, QTableWidgetItem(students[i][5]))
            self.table.setItem(i, 3, QTableWidgetItem(students[i][1]))
            self.table.setItem(i, 4, QTableWidgetItem(students[i][2]))
            self.table.setItem(i, 5, QTableWidgetItem(students[i][-1]))

        del sqllocal

    # Add New Students
    def AddNewStudent(self, e):
        newstudent = StudentDetails.StudentDetails()
        newstudent.exec_()
        if newstudent.allOkStatus:
            self.refreshStudentsTable()

    # Edit Student
    def EditStudent(self, e):
        if self.isConnectedToInternet() != 200:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You are not connected to the internet. The student will be able to login to the mobile app '
                        'only when you update the cloud database which will be updated when you connect to the '
                        'internet. Do you still wish to continue? ')
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                return

        ids = self.getCheckedRowIDs()
        if ids.__len__() != 1:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You can only update single student data at a time. Please select a single student '
                        'and try again')
            msg.exec_()
            return

        print("Edit Student")

    # Edit Subscription
    def EditSubscription(self, e):
        if self.isConnectedToInternet() != 200:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You are not connected to the internet. The student will be able to login to the mobile app '
                        'only when you update the cloud database which will be updated when you connect to the '
                        'internet. Do you still wish to continue? ')
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                return

        ids = self.getCheckedRowIDs()
        if ids.__len__() != 1:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You can only update subscription data one student at a time. '
                        'Please select a single student and try again')
            msg.exec_()
            return

        print("Subscription")

    # Delete Student
    def DeleteStudent(self, e):
        ids = self.getCheckedRowIDs()
        if ids.__len__() <= 0:
            return

        if self.isConnectedToInternet() != 200:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You are not connected to the internet. The student will be able to login to the mobile app '
                        'only when you update the cloud database which will be updated when you connect to the '
                        'internet. Do you still wish to continue? ')
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                return

        # [('ID-2932-0f23a6df', 'Subhamoy Karmakar')]
        for tmpID in ids:
            print(tmpID[0])
            print(tmpID[1])
            print("========================")

    # Send Custom Notification to Students
    def SendNotificationToStudent(self, e):
        if self.isConnectedToInternet() != 200:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You are not connected to the internet. Sending notification to students if '
                        'you are offline is not possible. Please connect to a network and try again.')
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                return
        ids = self.getCheckedRowIDs()
        print("Send Notification to Student : ", ids)

    # change the checkbox state on double click
    def onCellDoubleClickAction(self, r, c):
        if not self.table.cellWidget(r, 0).isChecked():
            self.table.cellWidget(r, 0).setChecked(True)
        else:
            self.table.cellWidget(r, 0).setChecked(False)

    # Get student IDs of checked rows
    def getCheckedRowIDs(self):
        sid = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).isChecked():
                sid.append((self.table.item(i, 1).text(), self.table.item(i, 2).text()))
            else:
                pass
        return sid

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
