from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Configuration as cfg
from Helper import *
import students.SQLTabStudents as SQLTabStudents
import students.FBTabStudents as FBTabStudents


class StudentDetails(QWidget):
    def __init__(self, student):
        super(StudentDetails, self).__init__()

        self.student = student

        self.sql = SQLTabStudents.SQLTabStudents()
        self.fb = FBTabStudents.FBTabStudents()

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
        self.lblStudents = QLabel("Students")
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
        # self.layoutButtons.addWidget(self.btnEditStudents)
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

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        # self.layoutButtons.addStretch(0)
        self.layoutButtons.setAlignment(Qt.AlignTop)

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
        self.table.setColumnWidth(1, 70)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 300)
        self.table.setColumnWidth(4, 200)
        # self.table.setColumnWidth(4, 300)

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
        self.btnEditStudents.mousePressEvent = self.EditSubscription
        self.btnDeleteStudents.mousePressEvent = self.DeleteStudent
        self.btnSendNotifStudents.mousePressEvent = self.SendNotificationToStudent

    def refreshStudentsTable(self):
        students = self.sql.getAllStudents()
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

    def AddNewStudent(self, e):
        print("Add Student")

    def EditStudent(self, e):
        print("Edit Student")

    def EditSubscription(self, e):
        print("Edit Subscription")

    def DeleteStudent(self, e):
        print("Delete Student")

    def SendNotificationToStudent(self, e):
        print("Send Notification to Student")






















