from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, os, datetime, time

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
import students.ShowAttendenceOfStudent as ShowAttendenceOfStudent


class TabStudent(QWidget):
    def __init__(self, tray):
        super(TabStudent, self).__init__()
        self.tray = tray
        self.threadStudent = ThreadLiveStudentSync(self.tray)
        self.threadStudent.update_student_data.connect(self.updateStudentTableFromThread)
        self.threadStudent.start()

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
        self.comboMembershipStatus = QComboBox()
        self.lblClearIcon = QLabel()
        self.pixMapICClear = QPixmap(cfg.IC_DELETE)
        self.table = QTableWidget()
        self.btnShowAttendence = QLabel()
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
        self.layoutSearch.addWidget(self.comboMembershipStatus)
        self.layoutSearch.addWidget(self.lblClearIcon)

        self.layoutButtons.addWidget(self.btnShowAttendence)
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

        self.comboMembershipStatus.clear()
        self.comboMembershipStatus.addItems(['All', 'Active', 'Expired'])

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

        self.btnShowAttendence.setPixmap(getPixMap(cfg.IC_SHOW_ATTENDENCE))
        self.btnShowAttendence.setCursor(Qt.PointingHandCursor)
        self.btnShowAttendence.setToolTip("Show Attendence")
        self.btnShowAttendence.setAlignment(Qt.AlignTop)

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
        self.btnShowAttendence.mousePressEvent = self.showAttendence
        self.btnSelectAll.mousePressEvent = self.selectAllRows
        self.btnNewStudents.mousePressEvent = self.AddNewStudent
        self.btnEditStudents.mousePressEvent = self.EditStudent
        self.btnSubscription.mousePressEvent = self.EditSubscription
        self.btnPunchIn.mousePressEvent = self.PunchInStudent
        self.btnDeleteStudents.mousePressEvent = self.DeleteStudent
        self.btnSendNotifStudents.mousePressEvent = self.SendNotificationToStudent
        self.lblClearIcon.mousePressEvent = self.clearSearchTermText
        self.lineEdtSearch.textChanged.connect(self.lineEdtSearchListener)
        self.comboMembershipStatus.currentIndexChanged.connect(self.comboBoxMembershipStatusChanged)

    def updateStudentTableFromThread(self, t):
        if t:
            self.refreshStudentsTable()

    def refreshStudentsTable(self):
        sqllocal = SQLTabStudents.SQLTabStudents()
        students = sqllocal.getAllStudents()
        self.table.clearContents()
        self.table.setRowCount(len(students))
        for i in range(len(students)):
            r = self.checkMembershipExpiryStatus(students[i][2])

            checkBox = QCheckBox()
            self.table.setCellWidget(i, 0, checkBox)
            self.table.setItem(i, 1, QTableWidgetItem(students[i][0]))
            self.table.setItem(i, 2, QTableWidgetItem(students[i][5]))
            self.table.setItem(i, 3, QTableWidgetItem(students[i][1]))
            self.table.setItem(i, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
            self.table.setItem(i, 5, QTableWidgetItem(students[i][-1]))
            if r == 0:
                self.table.setItem(i, 6, QTableWidgetItem('Expired'))
                self.table.item(i, 6).setBackground(QColor(255, 0, 0))
            else:
                self.table.setItem(i, 6, QTableWidgetItem('Active'))
            # self.table.setItem(i, 6, QTableWidgetItem(self.regStatus[students[i][6]]))

        del sqllocal

    def checkMembershipExpiryStatus(self, d):
        d = d.split('-')
        expiredate = datetime.date(
            int(d[0]), int(d[1]), int(d[2])
        )
        # n = datetime.da
        nowdate = datetime.date.today()
        datediff = expiredate - nowdate
        datediff = str(datediff)
        datediff = int(datediff[:datediff.index('day')].strip(' '))
        if datediff <= 0:
            return 0
        return 1

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

        # [('ID-2932-5d8d6b34', 'Test 1 '), ('ID-2932-7e24dabd', 'Subhamoy Karmakar'),
        # ('ID-2932-da96eb71', 'Elon TRON Musk')]
        ids = self.getCheckedRowIDs()
        notif = SendNotificationToStudent.SendNotificationToStudent(ids)
        notif.exec_()

    # show attendence of a student
    def showAttendence(self, e):
        ids = self.getCheckedRowIDs()
        if ids.__len__() != 1:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert!")
            if ids.__len__() <= 0:
                msg.setText('You will have to select at least one student to perform delete action. You can double click '
                            'on a row or, check the checkbox on the left most column in the table to select the '
                            'student(s).')
            else:
                msg.setText(
                    'You can select atmost one student to perform this action. Please select a '
                    'single student to continue!')
            msg.exec_()
            return
        attend = ShowAttendenceOfStudent.ShowAttendenceOfStudent(ids[0][0], ids[0][1])
        attend.exec_()

    # change the checkbox state on double click
    def onCellDoubleClickAction(self, r, c):
        if self.table.item(r, 1) is None:
            return

        if not self.table.cellWidget(r, 0).isChecked():
            self.table.cellWidget(r, 0).setChecked(True)
        else:
            self.table.cellWidget(r, 0).setChecked(False)

    # Get student IDs of checked rows
    def getCheckedRowIDs(self):
        sid = []
        for i in range(self.table.rowCount()):
            if self.table.item(i, 1) is None:
                continue

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
                if self.table.item(i, 1) is None:
                    continue
                self.table.cellWidget(i, 0).setChecked(False)
        else:
            self.selectAllStatus = True
            for i in range(self.table.rowCount()):
                if self.table.item(i, 1) is None:
                    continue
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

    def lineEdtSearchListener(self):
        membershipValidity = self.comboMembershipStatus.currentText().__str__()
        sqllocal = SQLTabStudents.SQLTabStudents()
        searchTerm = self.lineEdtSearch.text().__str__()

        students = sqllocal.searchTermQuery(searchTerm)
        self.table.clearContents()
        # self.table.setRowCount(0)
        self.table.setRowCount(len(students))
        cnt = 0
        for i in range(len(students)):
            r = self.checkMembershipExpiryStatus(students[i][2])
            if membershipValidity == 'All':
                # self.table.insertRow(cnt+1)
                checkBox = QCheckBox()
                self.table.setCellWidget(cnt, 0, checkBox)
                self.table.setItem(cnt, 1, QTableWidgetItem(students[i][0]))
                self.table.setItem(cnt, 2, QTableWidgetItem(students[i][5]))
                self.table.setItem(cnt, 3, QTableWidgetItem(students[i][1]))
                self.table.setItem(cnt, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
                self.table.setItem(cnt, 5, QTableWidgetItem(students[i][-1]))

                if r == 0:
                    self.table.setItem(cnt, 6, QTableWidgetItem('Expired'))
                    self.table.item(cnt, 6).setBackground(QColor(255, 0, 0))
                else:
                    self.table.setItem(cnt, 6, QTableWidgetItem('Active'))
                cnt += 1
            elif membershipValidity == 'Active' and r != 0:
                # self.table.insertRow(cnt+1)
                checkBox = QCheckBox()
                self.table.setCellWidget(cnt, 0, checkBox)
                self.table.setItem(cnt, 1, QTableWidgetItem(students[i][0]))
                self.table.setItem(cnt, 2, QTableWidgetItem(students[i][5]))
                self.table.setItem(cnt, 3, QTableWidgetItem(students[i][1]))
                self.table.setItem(cnt, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
                self.table.setItem(cnt, 5, QTableWidgetItem(students[i][-1]))
                self.table.setItem(cnt, 6, QTableWidgetItem('Active'))
                cnt += 1
            elif membershipValidity == 'Expired' and r == 0:
                # self.table.insertRow(cnt+1)
                checkBox = QCheckBox()
                self.table.setCellWidget(cnt, 0, checkBox)
                self.table.setItem(cnt, 1, QTableWidgetItem(students[i][0]))
                self.table.setItem(cnt, 2, QTableWidgetItem(students[i][5]))
                self.table.setItem(cnt, 3, QTableWidgetItem(students[i][1]))
                self.table.setItem(cnt, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
                self.table.setItem(cnt, 5, QTableWidgetItem(students[i][-1]))
                self.table.setItem(cnt, 6, QTableWidgetItem('Expired'))
                self.table.item(cnt, 6).setBackground(QColor(255, 0, 0))
                cnt += 1

    def comboBoxMembershipStatusChanged(self):
        sqllocal = SQLTabStudents.SQLTabStudents()
        searchTerm = self.lineEdtSearch.text().__str__()
        students = sqllocal.searchTermQuery(searchTerm)
        self.table.clearContents()
        self.table.setRowCount(len(students))
        cnt = 0
        if self.comboMembershipStatus.currentText() == 'All':
            for i in range(len(students)):
                r = self.checkMembershipExpiryStatus(students[i][2])
                # self.table.insertRow(1)
                checkBox = QCheckBox()
                self.table.setCellWidget(i, 0, checkBox)
                self.table.setItem(i, 1, QTableWidgetItem(students[i][0]))
                self.table.setItem(i, 2, QTableWidgetItem(students[i][5]))
                self.table.setItem(i, 3, QTableWidgetItem(students[i][1]))
                self.table.setItem(i, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
                self.table.setItem(i, 5, QTableWidgetItem(students[i][-1]))
                if r == 0:
                    self.table.setItem(i, 6, QTableWidgetItem('Expired'))
                    self.table.item(i, 6).setBackground(QColor(255, 0, 0))
                else:
                    self.table.setItem(i, 6, QTableWidgetItem('Active'))
        elif self.comboMembershipStatus.currentText() == 'Active':
            for i in range(len(students)):
                r = self.checkMembershipExpiryStatus(students[i][2])
                if r == 0:
                    continue
                # self.table.insertRow(1)
                checkBox = QCheckBox()
                self.table.setCellWidget(cnt, 0, checkBox)
                self.table.setItem(cnt, 1, QTableWidgetItem(students[i][0]))
                self.table.setItem(cnt, 2, QTableWidgetItem(students[i][5]))
                self.table.setItem(cnt, 3, QTableWidgetItem(students[i][1]))
                self.table.setItem(cnt, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
                self.table.setItem(cnt, 5, QTableWidgetItem(students[i][-1]))
                self.table.setItem(cnt, 6, QTableWidgetItem('Active'))
                cnt += 1

        elif self.comboMembershipStatus.currentText() == 'Expired':
            for i in range(len(students)):
                r = self.checkMembershipExpiryStatus(students[i][2])
                if r != 0:
                    continue
                # self.table.insertRow(1)
                checkBox = QCheckBox()
                self.table.setCellWidget(cnt, 0, checkBox)
                self.table.setItem(cnt, 1, QTableWidgetItem(students[i][0]))
                self.table.setItem(cnt, 2, QTableWidgetItem(students[i][5]))
                self.table.setItem(cnt, 3, QTableWidgetItem(students[i][1]))
                self.table.setItem(cnt, 4, QTableWidgetItem(self.convertSQLDateFormatToCustom(students[i][2])))
                self.table.setItem(cnt, 5, QTableWidgetItem(students[i][-1]))
                self.table.setItem(cnt, 6, QTableWidgetItem('Expired'))
                self.table.item(cnt, 6).setBackground(QColor(255, 0, 0))
                cnt += 1

    def clearSearchTermText(self, e):
        self.lineEdtSearch.clear()
        self.comboMembershipStatus.setCurrentIndex(0)
        self.refreshStudentsTable()

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


# LIVE NOTIFICATION SYSTEM
class ThreadLiveStudentSync(QThread):
    update_student_data = pyqtSignal(bool)

    def __init__(self, tray):
        super(ThreadLiveStudentSync, self).__init__()
        self.tray = tray

    def run(self):
        fb = FBTabStudents
        sql = SQLTabStudents.SQLTabStudents()
        gymid = sql.getGymId()
        while True:
            if self.isConnectedToInternet() != 200:
                print('TabStudent().Thread() - Not Connected to internet!')
                time.sleep(60)
                continue

            print('TabStudent().Thread() - Connected to internet!')
            data = fb.getAllStudentsData(gymid)
            localStudent = sql.getAllStudents()

            fbStudents = {}
            sqlStudents = {}

            for d in data:
                fbStudents[d[cfg.FB_KEY_STUDENTS_SID]] = d

            for s in localStudent:
                sqlStudents[s[0]] = s

            del data
            del localStudent

            resFirstInstall = sql.getFirstInstallFlagStudent()
            if resFirstInstall == "0":
                r = sql.insertStudentsAlternate(fbStudents)
                if r == 0:
                    sql.updateFirstInstallFlagStudent()
            else:
                # Delete from FB
                if sqlStudents.keys().__len__() < fbStudents.keys().__len__():
                    for id in fbStudents.keys():
                        if id not in sqlStudents.keys():
                            fb.deleteStudent(id)

                # Insert into FB
                if sqlStudents.keys().__len__() > fbStudents.keys().__len__():
                    for id in sqlStudents.keys():
                        if id not in fbStudents.keys():
                            tmpS = sqlStudents[id]
                            student = {
                                cfg.KEY_STUDENTS_SID: id,
                                cfg.KEY_STUDENTS_ALLOTTED_TIME: tmpS[1],
                                cfg.KEY_STUDENTS_MEMBERSHIP: tmpS[2],
                                cfg.KEY_STUDENTS_PHONE: tmpS[3],
                                cfg.KEY_STUDENTS_AGE: tmpS[4],
                                cfg.KEY_STUDENTS_NAME: tmpS[5],
                                cfg.KEY_STUDENTS_REG_STATUS: tmpS[6],
                                cfg.KEY_STUDENTS_DUE: tmpS[7]
                            }
                            fb.insertStudents(student)
                            del student

                # Validate All data
                for id in sqlStudents.keys():
                    tmpFB = fbStudents[id]
                    tmpSQL = sqlStudents[id]
                    status = True
                    if status and tmpFB[cfg.FB_KEY_STUDENTS_ALLOTTED_TIME] != tmpSQL[1]:
                        status = False

                    if status and tmpFB[cfg.FB_KEY_STUDENTS_MEMBERSHIP] != tmpSQL[2]:
                        status = False

                    if status and tmpFB[cfg.FB_KEY_STUDENTS_PHONE] != tmpSQL[3]:
                        status = False

                    if status and tmpFB[cfg.FB_KEY_STUDENTS_AGE] != tmpSQL[4]:
                        status = False

                    if status and tmpFB[cfg.FB_KEY_STUDENTS_NAME] != tmpSQL[5]:
                        status = False

                    if status and tmpFB[cfg.FB_KEY_STUDENTS_REG_STATUS] != tmpSQL[6]:
                        status = False

                    if status and tmpFB[cfg.DB_KEY_STUDENTS_DUE] != tmpSQL[7]:
                        status = False

                    if not status:
                        student = {
                            cfg.KEY_STUDENTS_SID: id,
                            cfg.KEY_STUDENTS_ALLOTTED_TIME: tmpSQL[1],
                            cfg.KEY_STUDENTS_MEMBERSHIP: tmpSQL[2],
                            cfg.KEY_STUDENTS_PHONE: tmpSQL[3],
                            cfg.KEY_STUDENTS_AGE: tmpSQL[4],
                            cfg.KEY_STUDENTS_NAME: tmpSQL[5],
                            cfg.KEY_STUDENTS_REG_STATUS: tmpSQL[6],
                            cfg.KEY_STUDENTS_DUE: tmpSQL[7]
                        }
                        fb.updateStudents(student)
                        del student

            self.update_student_data.emit(True)

            time.sleep(60 * 60)

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
