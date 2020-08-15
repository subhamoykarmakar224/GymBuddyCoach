from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import uuid, shutil, os, datetime, time, requests, calendar

import Configuration as cfg
from Helper import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents
from CustomMessageBox import *


class SubscriptionControl(QDialog):
    def __init__(self, sid):
        super(SubscriptionControl, self).__init__()
        self.sid = sid
        self.profilePath = ''
        self.photoChange = False
        self.validityCounter = 0
        if os.path.exists(cfg.TMP_FILE_PHOTO_DIR + sid + '.png'):
            self.profilePath = cfg.TMP_FILE_PHOTO_DIR + sid + '.png'
        elif os.path.exists(cfg.TMP_FILE_PHOTO_DIR + sid + '.jpg'):
            self.profilePath = cfg.TMP_FILE_PHOTO_DIR + sid + '.jpg'
        elif os.path.exists(cfg.TMP_FILE_PHOTO_DIR + sid + '.jpeg'):
            self.profilePath = cfg.TMP_FILE_PHOTO_DIR + sid + '.jpeg'

        self.regStatus = {
            'Disabled': 0,
            'Enabled': 1,
            'Blocked': -1
        }
        self.allOkStatus = False
        self.setWindowTitle(cfg.APP_NAME + " : Subscription Control")
        self.setFixedWidth(800)
        # self.setFixedHeight(520)
        self.setContentsMargins(20, 20, 20, 20)

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutButtons = QHBoxLayout()
        self.layoutExtendValidity = QHBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblStudentSID = QLabel('Student ID')
        self.imgProfilePhoto = QLabel()
        self.btnAddPhoto = QPushButton("Edit Photo")
        self.editTextSID = QLineEdit()
        self.editTextName = QLineEdit()
        self.editTextLastName = QLineEdit()
        self.datePickerDOB = QDateEdit(calendarPopup=True)
        self.editTextPhone = QLineEdit()
        self.editTextCurrentMembership = QLineEdit('')
        self.btnRefreshSubscription = QPushButton()
        self.btnAddSubscription = QPushButton()
        self.btnSubSubscription = QPushButton()
        self.editTextNewMembership = QDateEdit(calendarPopup=True)
        self.datePicker = QDateEdit(calendarPopup=True)
        self.startTimePicker = QTimeEdit()
        self.endTimePicker = QTimeEdit()
        self.editTextAmountDue = QLineEdit()
        self.regStatusComboBox = QComboBox()
        self.btnSave = QPushButton('Save')
        self.btnCancel = QPushButton('Cancel')

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutButtons.addWidget(self.btnSave, 0, Qt.AlignRight)
        self.layoutButtons.addWidget(self.btnCancel, 0, Qt.AlignLeft)
        self.layoutExtendValidity.addWidget(self.editTextNewMembership)
        self.layoutExtendValidity.addWidget(self.btnRefreshSubscription)
        self.layoutExtendValidity.addWidget(self.btnAddSubscription)
        self.layoutExtendValidity.addWidget(self.btnSubSubscription)

        # Add to Main Layout
        self.mainLayout.addWidget(self.imgProfilePhoto, 0, 0, 3, 1)

        self.mainLayout.addWidget(self.lblStudentSID, 0, 1)
        self.mainLayout.addWidget(self.editTextSID, 0, 2)
        self.mainLayout.addWidget(QLabel('Name'), 1, 1)
        self.mainLayout.addWidget(self.editTextName, 1, 2)
        self.mainLayout.addWidget(QLabel('Current Membership Till'), 2, 1)
        self.mainLayout.addWidget(self.editTextCurrentMembership, 2, 2)
        self.mainLayout.addWidget(QLabel('New Membership Extension'), 3, 1)
        self.mainLayout.addLayout(self.layoutExtendValidity, 3, 2)
        self.mainLayout.addWidget(QLabel('Registration Status'), 4, 1)
        self.mainLayout.addWidget(self.regStatusComboBox, 4, 2)
        self.mainLayout.addWidget(QLabel('Amount Due (INR)'), 5, 1)
        self.mainLayout.addWidget(self.editTextAmountDue, 5, 2)
        self.mainLayout.addLayout(self.layoutButtons, 6, 2)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

    def setLayoutProperties(self):
        self.mainLayout.setAlignment(Qt.AlignTop)

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        sql = SQLTabStudents.SQLTabStudents()
        sid = self.sid
        student = sql.getStudentInfo(sid)
        if student == {}:
            self.close()

        # SET :: PROFILE PHOTO
        self.btnAddPhoto.setIcon(QIcon(cfg.IC_ADD))
        self.btnAddPhoto.setFixedHeight(50)

        if self.profilePath == '':
            profilePhotoPixMap = QPixmap(cfg.IC_ADD_PHOTO)
        else:
            profilePhotoPixMap = QPixmap(self.profilePath)

        self.imgProfilePhoto.setPixmap(profilePhotoPixMap.scaled(100, 100, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.imgProfilePhoto.setCursor(Qt.PointingHandCursor)
        self.imgProfilePhoto.setToolTip("add profile image")

        self.lblStudentSID.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnRefreshSubscription.setText("Refresh")
        self.btnRefreshSubscription.setIcon(QIcon(cfg.IC_REFRESH_COLOR))
        self.btnRefreshSubscription.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnAddSubscription.setText("Add Months")
        self.btnAddSubscription.setIcon(QIcon(cfg.IC_ADD_COLOR))
        self.btnAddSubscription.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnSubSubscription.setText("Sub Months")
        self.btnSubSubscription.setIcon(QIcon(cfg.IC_SUB_COLOR))
        self.btnSubSubscription.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # SET :: NAME
        self.editTextName.setText(student[cfg.KEY_STUDENTS_NAME])
        self.editTextName.setReadOnly(True)

        # SET :: CURRENT MEMBERSHIP VALIDITY
        membership = student[cfg.KEY_STUDENTS_MEMBERSHIP]
        self.editTextCurrentMembership.setReadOnly(True)
        self.editTextCurrentMembership.setText(self.convertSQLDateFormatToCustom(membership))

        # SET : New membership data
        self.editTextNewMembership.setDisplayFormat('dd MMMM, yyyy')
        tmpMembership = membership.split('-')
        tmpMembership = [int(m) for m in tmpMembership]
        try:
            tmpQDate = QDate()
            tmpQDate.setDate(tmpMembership[0], tmpMembership[1], tmpMembership[2])
            self.editTextNewMembership.setDate(tmpQDate)
        except Exception as e:
            print(e)
            return

        # SET : REGISTRATION STATUS
        self.regStatusComboBox.clear()
        self.regStatusComboBox.addItems(self.regStatus.keys())
        opt = ''
        for k in self.regStatus.keys():
            if str(self.regStatus[k]) == student[cfg.KEY_STUDENTS_REG_STATUS]:
                opt = k
                break
        if opt == '':
            self.regStatusComboBox.setCurrentIndex(0)
        else:
            self.regStatusComboBox.setCurrentIndex(list(self.regStatus.keys()).index(opt))

        self.editTextAmountDue.setText(student[cfg.KEY_STUDENTS_DUE])

        self.editTextSID.setText(self.sid)
        self.editTextSID.setReadOnly(True)

        self.btnSave.setFixedWidth(80)
        self.btnSave.setFixedHeight(50)
        self.btnCancel.setFixedWidth(80)
        self.btnCancel.setFixedHeight(50)

    def setListeners(self):
        self.btnCancel.clicked.connect(self.cancelStudent)
        self.btnSave.clicked.connect(self.saveStudent)
        self.btnRefreshSubscription.clicked.connect(self.refreshValidityDate)
        self.btnAddSubscription.clicked.connect(self.increaseValidityByOneMonth)
        self.btnSubSubscription.clicked.connect(self.decreaseValidityByOneMonth)

    def cancelStudent(self):
        self.close()

    # Checks if the user presses cancel button
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.cancelStudent()

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

    # Save Student
    def saveStudent(self):
        status, student = self.validateFields()
        if not status:
            return

        sql = SQLTabStudents.SQLTabStudents()
        res = sql.updateStudentMembershipInfo(student)

        if res == 0:
            if self.isConnectedToInternet() == 200:
                FBTabStudents.updateStudents(student)

        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Saved")
        msg.setText("Student Data has been updated!")
        msg.exec_()
        self.allOkStatus = True
        self.close()

    # Validates fields
    def validateFields(self):
        status = True
        student = {}
        sid = self.editTextSID.text().__str__()
        oldmembership = self.editTextCurrentMembership.text().__str__()
        newmembership = self.editTextNewMembership.text().__str__()
        regstatus = self.regStatusComboBox.currentText().__str__()
        due = self.editTextAmountDue.text().__str__()

        # Membership
        datediff = self.getNoOfMembershipDays(newmembership, oldmembership)
        msg = CustomInfoMessageBox()
        if datediff < 0:
            msg.setWindowTitle("Alert")
            msg.setText("You are about to set the new membership date to " + str(-1 * datediff) +
                        " months previous to current membership expiry value. Are you sure you want to continue?")
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                status = False
                return status, student
        else:
            msg.setWindowTitle("Alert")
            msg.setText("Are you sure you want to extend the membership validity for " + str(datediff) +
                        " month(s), till " + newmembership + " ?")
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                status = False
                return status, student

        # Registration Status
        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Alert")
        msg.setText("Are you sure you want to set the membership status to- " + regstatus + "?")
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        r = msg.exec_()
        if r == QMessageBox.No:
            status = False
            return status, student

        # Due amount
        try:
            tmp = int(due)
        except:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("The due amount you have entered is invalid!")
            r = msg.exec_()
            status = False
            return status, student

        student = {
            cfg.KEY_STUDENTS_SID: sid,
            cfg.KEY_STUDENTS_MEMBERSHIP: self.convertToSQLDateFormat(newmembership),
            cfg.KEY_STUDENTS_REG_STATUS: str(self.regStatus[regstatus]),
            cfg.KEY_STUDENTS_DUE: str(due)
        }
        return status, student

    # On Click Refresh Button sets the new validity date to current membership value
    def refreshValidityDate(self):
        oldValidity = self.convertToSQLDateFormat(self.editTextCurrentMembership.text())

        tmpMembership = oldValidity.split('-')
        tmpMembership = [int(m) for m in tmpMembership]
        try:
            tmpQDate = QDate()
            tmpQDate.setDate(tmpMembership[0], tmpMembership[1], tmpMembership[2])
            self.editTextNewMembership.setDate(tmpQDate)
        except Exception as e:
            print(e)
            return

    # Increases the date by one month
    def increaseValidityByOneMonth(self):
        self.validityCounter += 1
        self.setNewValidityDateField()

    # Decrease the date by one month
    def decreaseValidityByOneMonth(self):
        self.validityCounter -= 1
        self.setNewValidityDateField()

    # Sets the date in the required format to the new membership date
    def setNewValidityDateField(self):
        currentValidity = self.editTextCurrentMembership.text().__str__().strip()
        currentValidity = self.convertToSQLDateFormat(currentValidity).split('-')
        currentValidity = [int(i) for i in currentValidity]
        sourcedate = datetime.date(currentValidity[0], currentValidity[1], currentValidity[2])
        month = sourcedate.month - 1 + self.validityCounter
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        newValidity = datetime.date(year, month, day).__format__('%Y-%m-%d')

        tmpMembership = newValidity.split('-')
        tmpMembership = [int(m) for m in tmpMembership]
        try:
            tmpQDate = QDate()
            tmpQDate.setDate(tmpMembership[0], tmpMembership[1], tmpMembership[2])
            self.editTextNewMembership.setDate(tmpQDate)
        except Exception as e:
            print(e)
            return

    def calculateAge(self, birthDate):
        tmp = self.convertToSQLDateFormat(birthDate).split("-")
        birthDate = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
        today = datetime.date.today()
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    def getNoOfMembershipDays(self, start, end):
        start = self.convertToSQLDateFormat(start)
        start = start.split('-')
        start = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        end = self.convertToSQLDateFormat(end)
        end = end.split('-')
        end = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        datediff =  str(end - start)
        try:
            datediff = start.month - end.month + 12*(start.year - end.year)
        except:
            return 0

        return datediff

    def convertToSQLDateFormat(self, s):
        inFormat = '%d %B, %Y'
        sqlFormat = '%Y-%m-%d'
        s = datetime.datetime.strptime(s, inFormat).strftime(sqlFormat)
        return s

    def convertSQLDateFormatToCustom(self, s):
        sqlFormat = '%Y-%m-%d'
        inFormat = '%d %B, %Y'
        s = datetime.datetime.strptime(s, sqlFormat).strftime(inFormat)
        return s

    def convertTo12HrsFormat(self, t):
        t = time.strptime(t, "%H:%M")
        return time.strftime("%I:%M %p", t)

    def convertTo24HrsFormat(self, t):
        t = time.strptime(t, "%I:%M %p")
        return time.strftime("%H:%M", t)

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
