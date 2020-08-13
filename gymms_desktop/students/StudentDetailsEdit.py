from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import uuid, shutil, os, datetime, time, requests

import Configuration as cfg
from Helper import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents
from CustomMessageBox import *


class StudentDetailsEdit(QDialog):
    def __init__(self, sid):
        super(StudentDetailsEdit, self).__init__()
        self.sid = sid
        self.profilePath = ''
        self.photoChange = False
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
        self.setWindowTitle(cfg.APP_NAME + " : Edit Student Information")
        self.setFixedWidth(800)
        self.setFixedHeight(520)
        self.setContentsMargins(20, 20, 20, 20)

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutButtons = QHBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.imgProfilePhoto = QLabel()
        self.btnAddPhoto = QPushButton("Edit Photo")
        self.editTextSID = QLineEdit()
        self.editTextFirstName = QLineEdit()
        self.editTextLastName = QLineEdit()
        self.datePickerDOB = QDateEdit(calendarPopup=True)
        self.editTextPhone = QLineEdit()
        self.editTextCurrentMembership = QLabel("")
        self.btnAddSubscription = QPushButton("Add Subscription")
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

        # Add to Main Layout
        self.mainLayout.addWidget(self.imgProfilePhoto, 0, 0, 3, 1)
        self.mainLayout.addWidget(self.btnAddPhoto, 3, 0)

        self.mainLayout.addWidget(QLabel('Student ID'), 0, 1)
        self.mainLayout.addWidget(self.editTextSID, 1, 1)
        self.mainLayout.addWidget(QLabel('First Name'), 2, 1)
        self.mainLayout.addWidget(self.editTextFirstName, 3, 1)
        self.mainLayout.addWidget(QLabel('Last Name'), 2, 2)
        self.mainLayout.addWidget(self.editTextLastName, 3, 2)
        self.mainLayout.addWidget(QLabel('Date of Birth'), 4, 1)
        self.mainLayout.addWidget(self.datePickerDOB, 5, 1)
        self.mainLayout.addWidget(QLabel('Contact'), 4, 2)
        self.mainLayout.addWidget(self.editTextPhone, 5, 2)
        self.mainLayout.addWidget(QLabel('Start Time (24-hrs format)'), 6, 1)
        self.mainLayout.addWidget(QLabel('End Time (24-hrs format)'), 6, 2)
        self.mainLayout.addWidget(self.startTimePicker, 7, 1)
        self.mainLayout.addWidget(self.endTimePicker, 7, 2)
        self.mainLayout.addWidget(QLabel('Current Membership Till'), 8, 1)
        self.mainLayout.addWidget(self.editTextCurrentMembership, 9, 1)
        self.mainLayout.addWidget(%, 9, 1)
        self.mainLayout.addWidget(self.editTextCurrentMembership, 9, 1)


        # self.mainLayout.addWidget(QLabel('Registration Status'), 8, 2)
        # self.mainLayout.addWidget(self.regStatusComboBox, 9, 2)

        # self.mainLayout.addWidget(QLabel('Amount Due (INR)'), 10, 1)
        # self.mainLayout.addWidget(self.editTextAmountDue, 11, 1)
        self.mainLayout.addLayout(self.layoutButtons, 12, 2)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

    def setLayoutProperties(self):
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setRowMinimumHeight(6, 50)
        self.mainLayout.setRowMinimumHeight(8, 50)
        self.mainLayout.setRowMinimumHeight(10, 50)

    def setSubLayoutProperties(self):
        pass
        # self.layoutButtons.add

    def setWidgetProperties(self):
        sql = SQLTabStudents.SQLTabStudents()
        sid = self.sid
        student = sql.getStudentInfo(sid)
        if student == {}:
            self.close()

        # {'SID': 'ID-2932-da96eb71', 'allotedtime': '06:00 AM to 08:00 AM',
        # 'membershipvalidity': '2020-09-13', 'phone': '+916549873210',
        # 'studentage': '1976-03-04', 'studentname': 'Elon Musk', 'regstatus': '1',
        # 'dueamount': '0'}

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

        # SET :: FIRST NAME and LAST NAME
        name = student[cfg.KEY_STUDENTS_NAME].split(' ')
        self.editTextFirstName.setText(' '.join(name[:len(name) - 1]))
        self.editTextLastName.setText(name[::-1][0])

        # SET :: CURRENT MEMBERSHIP VALIDITY
        membership = student[cfg.KEY_STUDENTS_MEMBERSHIP]
        self.editTextCurrentMembership.setText(self.convertSQLDateFormatToCustom(membership))


        self.datePicker.setDateTime(QDateTime.currentDateTime())
        self.datePicker.setMinimumDate(QDate.currentDate())
        self.datePicker.setDisplayFormat('dd MMMM, yyyy')
        # membership = student[cfg.KEY_STUDENTS_MEMBERSHIP].split("-")
        # membership = [int(m) for m in membership]
        # try:
        #     tmpQDate = QDate()
        #     tmpQDate.setDate(membership[0], membership[1], membership[2])
        #     self.datePicker.setDate(tmpQDate)
        # except Exception as e:
        #     print(e)
        #     return

        dob = student[cfg.KEY_STUDENTS_AGE].split("-") # 1976-03-04
        dob = [int(d) for d in dob]
        self.datePickerDOB.setDateTime(QDateTime.currentDateTime())
        self.datePickerDOB.setMaximumDate(QDate.currentDate())
        self.datePickerDOB.setDisplayFormat('dd MMMM, yyyy')
        try:
            tmpQDate = QDate()
            tmpQDate.setDate(dob[0], dob[1], dob[2])
            self.datePickerDOB.setDate(tmpQDate)
        except Exception as e:
            print(e)
            return

        phone = student[cfg.KEY_STUDENTS_PHONE]
        self.editTextPhone.setText(phone)

        startendtime = student[cfg.KEY_STUDENTS_ALLOTTED_TIME].split(" to ")
        startendtime[0] = self.convertTo24HrsFormat(startendtime[0]).split(":")
        startendtime[1] = self.convertTo24HrsFormat(startendtime[1]).split(":")
        self.startTimePicker.setDisplayFormat('HH:mm')
        self.startTimePicker.setTime(QTime(int(startendtime[0][0]), int(startendtime[0][1])))
        self.endTimePicker.setDisplayFormat('HH:mm')
        self.endTimePicker.setTime(QTime(int(startendtime[1][0]), int(startendtime[1][1])))

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
        self.editTextFirstName.setPlaceholderText("First Name")
        self.editTextLastName.setPlaceholderText("Last Name")
        self.editTextPhone.setPlaceholderText("Contact No.")

        self.btnSave.setFixedWidth(80)
        self.btnSave.setFixedHeight(50)
        self.btnCancel.setFixedWidth(80)
        self.btnCancel.setFixedHeight(50)

    def setListeners(self):
        self.btnAddPhoto.clicked.connect(self.loadStudentPhoto)
        self.btnSave.clicked.connect(self.saveStudent)
        self.btnCancel.clicked.connect(self.cancelStudent)

    def cancelStudent(self):
        self.close()

    # Load student photo
    def loadStudentPhoto(self):
        filePath = QFileDialog.getOpenFileName(filter = "*.jpg;*.png;*.jpeg")
        filePath = filePath[0]
        if filePath == '':
            return

        if self.profilePath != '' and os.path.isfile(self.profilePath) and self.photoChange:
            os.remove(self.profilePath)
            self.profilePath = ''

        self.photoChange = True

        extension = filePath[::-1]
        extension = extension[:extension.index('.')][::-1]
        self.profilePath = ''.join([cfg.TMP_FILE_DIR, self.editTextSID.text().__str__(), '.', extension])
        shutil.copyfile(filePath, self.profilePath)
        pixmap = QPixmap(self.profilePath)
        self.imgProfilePhoto.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))

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
            if self.profilePath != '' and os.path.isfile(self.profilePath) and self.photoChange:
                os.remove(self.profilePath)
                self.profilePath = ''
            event.accept()
        else:
            event.ignore()

    # Save Student
    def saveStudent(self):
        status, student = self.validateFields()
        if not status:
            return

        res = self.sql.insertStudents([student])
        if res == 0:
            if self.isConnectedToInternet() == 200:
                FBTabStudents.insertStudents(student)

            if self.profilePath != '':
                shutil.move(self.profilePath, cfg.TMP_FILE_PHOTO_DIR)

            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Saved")
            msg.setText("Student Data has been updated!")
            msg.exec_()
            self.allOkStatus = True
            self.close()
        else:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("There was an error saving the information. Please try again!")
            msg.exec_()

    # Validates fields
    def validateFields(self):
        status = True
        student = {}
        sid = self.editTextSID.text().__str__()
        firstname = self.editTextFirstName.text().__str__()
        lastname = self.editTextLastName.text().__str__()
        dob = self.datePickerDOB.text().__str__().replace("\,", "")
        phone = self.editTextPhone.text().__str__()
        starttime = self.startTimePicker.text().__str__()
        endtime = self.endTimePicker.text().__str__()
        membership = self.datePicker.text().__str__()
        regstatus = self.regStatusComboBox.currentText().__str__()
        due = self.editTextAmountDue.text().__str__()
        photo = self.profilePath.__str__()

        # First Name
        if firstname == "":
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("First name field cannot be left blank.")
            msg.exec_()
            status = False
            return status, student

        # Age
        age = self.calculateAge(dob)
        if age <= 5:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Age not valid. Please enter a valid age")
            msg.exec_()
            status = False
            return status, student
        if age >= 6:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("The age of the student is " + str(age) + ". Is that right?")
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                msg = CustomCriticalMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please check the Date of Birth field and try again.")
                msg.exec_()
                status = False
                return status, student

        # Phone no
        if phone.__len__() == 10:
            try:
                tmp = int(phone)
            except Exception as e:
                msg = CustomCriticalMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("The phone number you have entered is invalid. Please check the number.")
                msg.exec_()
                status = False
                return status, student
        else:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The phone number you have entered is invalid. Please check the number.")
            msg.exec_()
            status = False
            return status, student

        if self.sql.studentPhoneAlreadyPresentStatus("+91" + phone) != 0:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The phone number is already in use. Please check the number entered and try again.")
            msg.exec_()
            status = False
            return status, student

        # Alloted time
        FMT = '%H:%M'
        tdelta = str(datetime.datetime.strptime(endtime, FMT) - datetime.datetime.strptime(starttime, FMT))
        if tdelta == '0:00:00' or tdelta == '0:15:00' or (tdelta.__contains__('-') and tdelta.__contains__('day')):
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The alloted start time and end time you have entered is invalid. "
                        "Please check the values and try again.")
            msg.setDetailedText("Rules:\n1. The alloted time to any candidate should be minimum 15 minutes\n"
                                "2. End Time should be greater than Start Time value.")
            msg.exec_()
            status = False
            return status, student
        else:
            tmp = tdelta.split(":")
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Are you sure you want to allot " + tmp[0] + " hrs and " + tmp[1] +
                        " minutes starting from " + self.convertTo12HrsFormat(starttime) + " to " +
                        self.convertTo12HrsFormat(endtime) + " ?")
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                status = False
                return status, student

        # Membership
        datediff = self.getNoOfMembershipDays(membership)
        if datediff == 0:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The membership validity date you have entered is less invalid. "
                        "Please check the value and try again.")
            msg.exec_()
            status = False
            return status, student
        else:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Are you sure you want to extend the membership validity for " + str(datediff) +
                        " days, till " + membership + " ?")
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                status = False
                return status, student

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

        if self.profilePath == '':
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("You have not added any photo yet. Do you wish to proceed?")
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            r = msg.exec_()
            if r == QMessageBox.No:
                status = False
                return status, student

        student = {
            cfg.KEY_STUDENTS_SID: sid,
            cfg.KEY_STUDENTS_ALLOTTED_TIME: self.convertTo12HrsFormat(starttime) + " to " + self.convertTo12HrsFormat(endtime),
            cfg.KEY_STUDENTS_MEMBERSHIP: self.convertToSQLDateFormat(membership),
            cfg.KEY_STUDENTS_PHONE: "+91" + str(phone),
            cfg.KEY_STUDENTS_AGE: str(self.convertToSQLDateFormat(dob)),
            cfg.KEY_STUDENTS_NAME: str(firstname + " " + lastname),
            cfg.KEY_STUDENTS_REG_STATUS: str(self.regStatus[regstatus]),
            cfg.KEY_STUDENTS_DUE: str(due)

        }
        return status, student

    def calculateAge(self, birthDate):
        tmp = self.convertToSQLDateFormat(birthDate).split("-")
        birthDate = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
        today = datetime.date.today()
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    def getNoOfMembershipDays(self, m):
        start = datetime.date.today()
        end = self.convertToSQLDateFormat(m)
        end = end.split('-')
        end = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        datediff =  str(end - start)
        try:
            datediff = datediff[:datediff.index(" ")]
        except:
            return 0
        return int(datediff)

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