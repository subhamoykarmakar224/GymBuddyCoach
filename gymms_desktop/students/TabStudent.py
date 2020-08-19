from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, os, datetime

import Configuration as cfg
from Helper import *
from CustomMessageBox import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents
import students.StudentDetails as StudentDetails
import students.StudentDetailsEdit as StudentDetailsEdit
import students.SubscriptionControl as SubscriptionControl
import students.SendNotificationToStudent as SendNotificationToStudent
import students.PunchInStudent as PunchInStudent


class TabStudent(QWidget):
    def __init__(self):
        super(TabStudent, self).__init__()

        self.selectedStudent = []
        self.selectAllStatus = False
        self.regStatus = {
            '0':'Disabled',
            '1': 'Enabled',
            '-1': 'Blocked'
        }

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
        self.btnSelectAll = QLabel()
        self.btnNewStudents = QLabel()
        self.btnEditStudents = QLabel()
        self.btnSubscription = QLabel()
        self.btnPunchIn = QLabel()
        self.btnDeleteStudents = QLabel()
        self.btnSendNotifStudents = QLabel()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutSearch.addWidget(self.lineEdtSearch)
        self.layoutSearch.addWidget(self.lblClearIcon)

        self.layoutButtons.addWidget(self.btnSelectAll)
        self.layoutButtons.addWidget(self.btnNewStudents)
        self.layoutButtons.addWidget(self.btnEditStudents)
        self.layoutButtons.addWidget(self.btnSubscription)
        self.layoutButtons.addWidget(self.btnPunchIn)
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
        self.columnsHeaders = ['#', 'ID', 'Name', 'Alloted Time', 'Membership Validity', 'Due Amount', 'Status']
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

        self.btnSelectAll.setPixmap(getPixMap(cfg.IC_SELECT_ALL))
        self.btnSelectAll.setCursor(Qt.PointingHandCursor)
        self.btnSelectAll.setToolTip("Select/Deselect All")
        self.btnSelectAll.setAlignment(Qt.AlignTop)

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

        self.btnPunchIn.setPixmap(getPixMap(cfg.IC_PUNCH_IN))
        self.btnPunchIn.setCursor(Qt.PointingHandCursor)
        self.btnPunchIn.setToolTip("Manual Punch-In")
        self.btnPunchIn.setAlignment(Qt.AlignTop)

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
        self.btnSelectAll.mousePressEvent = self.selectAllRows
        self.btnNewStudents.mousePressEvent = self.AddNewStudent
        self.btnEditStudents.mousePressEvent = self.EditStudent
        self.btnSubscription.mousePressEvent = self.EditSubscription
        self.btnPunchIn.mousePressEvent = self.PunchInStudent
        self.btnDeleteStudents.mousePressEvent = self.DeleteStudent
        self.btnSendNotifStudents.mousePressEvent = self.SendNotificationToStudent

    def refreshStudentsTable(self):
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
            self.table.setItem(i, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
            self.table.setItem(i, 5, QTableWidgetItem(students[i][-1]))
            self.table.setItem(i, 6, QTableWidgetItem(self.regStatus[students[i][6]]))

        del sqllocal

    # Add New Students
    def AddNewStudent(self, e):
        newstudent = StudentDetails.StudentDetails()
        newstudent.exec_()
        if newstudent.allOkStatus:
            self.refreshStudentsTable()

    # Edit Student
    def EditStudent(self, e):
        ids = self.getCheckedRowIDs()
        if ids.__len__() != 1:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You can only update single student data at a time. Please select a single student '
                        'and try again')
            msg.exec_()
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

        editstudent = StudentDetailsEdit.StudentDetailsEdit(ids[0][0])
        editstudent.exec_()
        if editstudent.allOkStatus:
            self.refreshStudentsTable()

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

        s = SubscriptionControl.SubscriptionControl(ids[0][0])
        s.exec_()
        if s.allOkStatus:
            self.refreshStudentsTable()

    # Delete Student
    def DeleteStudent(self, e):
        ids = self.getCheckedRowIDs()
        if ids.__len__() <= 0:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You will have to select at least one student to perform delete action. You can double click '
                        'on a row or, check the checkbox on the left most column in the table to select the '
                        'student(s).')
            msg.exec_()
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

        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Alert!")
        msg.setText('You are about to delete the student from your database. Are you sure you want to proceed?')
        msg.setDetailedText('If your perform this action the information about this student will be lost forever. '
                            'Instead it is advised, you can keep his information in your database but change the '
                            '\"registration status\" field to either-\n1. Disabled or, \n2. Blocked')
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        r = msg.exec_()
        if r == QMessageBox.No:
            return

        sqllocal = SQLTabStudents.SQLTabStudents()

        # [('ID-2932-0f23a6df', 'Subhamoy Karmakar')]
        for tmpID in ids:
            sqllocal.deleteStudent(tmpID[0])
            if os.path.exists(cfg.TMP_FILE_PHOTO_DIR + tmpID[0] + '.png'):
                os.remove(cfg.TMP_FILE_PHOTO_DIR + tmpID[0] + '.png')
            elif os.path.exists(cfg.TMP_FILE_PHOTO_DIR + tmpID[0] + '.jpg'):
                os.remove(cfg.TMP_FILE_PHOTO_DIR + tmpID[0] + '.jpg')
            elif os.path.exists(cfg.TMP_FILE_PHOTO_DIR + tmpID[0] + '.jpeg'):
                os.remove(cfg.TMP_FILE_PHOTO_DIR + tmpID[0] + '.jpeg')

            FBTabStudents.deleteStudent(tmpID[0])

        # refresh table content
        self.refreshStudentsTable()

        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Done")
        msg.setText('Students information have been deleted.')
        msg.exec_()
        return

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

        # [('ID-2932-5d8d6b34', 'Test 1 '), ('ID-2932-7e24dabd', 'Subhamoy Karmakar'), ('ID-2932-da96eb71', 'Elon TRON Musk')]
        ids = self.getCheckedRowIDs()
        notif = SendNotificationToStudent.SendNotificationToStudent(ids)
        notif.exec_()

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

    # Select/Deselect all
    def selectAllRows(self, e):
        if self.selectAllStatus:
            self.selectAllStatus = False
            for i in range(self.table.rowCount()):
                self.table.cellWidget(i, 0).setChecked(False)
        else:
            self.selectAllStatus = True
            for i in range(self.table.rowCount()):
                self.table.cellWidget(i, 0).setChecked(True)

    def PunchInStudent(self, e):
        # [('ID-2932-7e24dabd', 'Subhamoy Karmakar'), ('ID-2932-da96eb71', 'Elon TRON Musk')]
        ids = self.getCheckedRowIDs()
        if ids.__len__() <= 0:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You will have to select a student to perform this action!')
            msg.exec_()
            return

        if ids.__len__() >= 2:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You cannot perform this action on multiple students. Due to security reasons you can only '
                        'change this one student at a time.')
            msg.exec_()
            return

        if self.isConnectedToInternet() != 200:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            msg.setText('You are not connected to the internet. Please connect to a network and try again! ')
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                return

        ids = ids[0][0]
        punchIn = PunchInStudent.PunchInStudent(ids)
        punchIn.exec_()

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code

    def convertSQLDateFormatToCustom(self, s):
        sqlFormat = '%Y-%m-%d'
        inFormat = '%d %B, %Y'
        s = datetime.datetime.strptime(s, sqlFormat).strftime(inFormat)
        return s
