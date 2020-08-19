from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import uuid, shutil, os, datetime, time, requests, calendar

import Configuration as cfg
from Helper import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as fb
from CustomMessageBox import *


class PunchInStudent(QDialog):
    def __init__(self, sid):
        super(PunchInStudent, self).__init__()
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
        self.setWindowTitle(cfg.APP_NAME + " : Manual Punch-in")
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

        self.datePickerPunchInDate = QDateEdit(calendarPopup=True)

        self.startTimePicker = QTimeEdit()
        self.endTimePicker = QTimeEdit()

        self.btnSave = QPushButton('Punch In')
        self.btnCancel = QPushButton('Cancel')

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutButtons.addWidget(self.btnSave, 0, Qt.AlignRight)
        self.layoutButtons.addWidget(self.btnCancel, 0, Qt.AlignLeft)

        # Add to Main Layout
        self.mainLayout.addWidget(self.imgProfilePhoto, 0, 0, 3, 1)

        self.mainLayout.addWidget(self.lblStudentSID, 0, 1)
        self.mainLayout.addWidget(self.editTextSID, 0, 2)
        self.mainLayout.addWidget(QLabel('Name'), 1, 1)
        self.mainLayout.addWidget(self.editTextName, 1, 2)
        self.mainLayout.addWidget(QLabel('Punch In Date'), 2, 1)
        self.mainLayout.addWidget(self.datePickerPunchInDate, 2, 2)
        self.mainLayout.addWidget(QLabel('Start Time'), 3, 1)
        self.mainLayout.addWidget(QLabel('End Time'), 3, 2)
        self.mainLayout.addWidget(self.startTimePicker, 4, 1)
        self.mainLayout.addWidget(self.endTimePicker, 4, 2)
        self.mainLayout.addLayout(self.layoutButtons, 5, 2)

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

        # SET :: NAME
        self.editTextName.setText(student[cfg.KEY_STUDENTS_NAME])
        self.editTextName.setReadOnly(True)

        # SET : Punch In date time
        self.datePickerPunchInDate.setFixedWidth(120)
        self.datePickerPunchInDate.setDisplayFormat('dd MMMM, yyyy')
        try:
            self.datePickerPunchInDate.setDate(QDate.currentDate())
        except Exception as e:
            print(e)
            return

        self.startTimePicker.setTime(QTime.currentTime())
        self.endTimePicker.setFixedWidth(80)
        self.endTimePicker.setTime(QTime.currentTime())

        self.editTextSID.setText(self.sid)
        self.editTextSID.setReadOnly(True)

        self.btnSave.setFixedWidth(80)
        self.btnSave.setFixedHeight(50)
        self.btnCancel.setFixedWidth(80)
        self.btnCancel.setFixedHeight(50)

    def setListeners(self):
        self.btnCancel.clicked.connect(self.cancelStudent)
        self.btnSave.clicked.connect(self.saveStudent)

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
        status = self.validateFields()
        if not status:
            return

        sql = SQLTabStudents.SQLTabStudents()

        gymId = sql.getGymId()
        counter = sql.getLastNotificationMsgCnt()[0]

        tmpDate = self.convertToSQLDateFormat(self.datePickerPunchInDate.text().__str__().strip(" "))
        tmpDate = cfg.NOTIF_MSG_ATTEND_PREFIX + tmpDate + " :: " + "1"

        # TODO :: Send Green Notification


        # TODO :: Notification Msg
        sql.sendNotificationsMsg([(self.sid, "")], tmpDate)
        fb.sendNotification(counter + 1, (self.sid, ""), tmpDate, gymId)

        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Saved")
        msg.setText("Student has been punched in!")
        msg.exec_()
        self.allOkStatus = True
        self.close()

    # Validates fields
    def validateFields(self):
        startTime = self.startTimePicker.text().__str__()
        endTime = self.endTimePicker.text().__str__()
        tmpStartTime = self.convertTo24HrsFormat(startTime).split(":")
        tmpEndTime = self.convertTo24HrsFormat(endTime).split(":")
        tmpStartTime = datetime.datetime(2020, 1, 1, int(tmpStartTime[0]), int(tmpStartTime[1]), 0)
        tmpEndTime = datetime.datetime(2020, 1, 1, int(tmpEndTime[0]), int(tmpEndTime[1]), 0)

        timeDelta = str(tmpEndTime - tmpStartTime)

        if timeDelta.__contains__("day,") and timeDelta.__contains__("-"):
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("The start time you have entered is more than the end time of the workout session. "
                        "Please check the times and try agains.")
            msg.exec_()
            return False

        if timeDelta == "0:00:00":
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("The time you have entered is invalid. The duration of workout can be minimum of 20 mins")
            msg.exec_()
            return False

        timeDelta = timeDelta.split(":")
        timeDelta = [int(t) for t in timeDelta]
        if timeDelta[0] == 0 and timeDelta[1] < 20:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("The time you have entered is invalid. The duration of workout can be minimum of 20 mins")
            msg.exec_()
            return False

        return True

    def convertToSQLDateFormat(self, s):
        inFormat = '%d %B, %Y'
        sqlFormat = '%d-%m-%Y'
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
