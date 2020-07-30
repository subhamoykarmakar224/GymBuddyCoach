from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg


# Student Dash
class StudentView(QWidget):
    def __init__(self, studentName):
        super(StudentView, self).__init__()
        self.studentName = studentName

        # Main Layout
        self.grid = QVBoxLayout(self)
        self.scrollArea = QScrollArea()

        # Sub Layout
        self.hBoxGenderLayout = QHBoxLayout()

        # Widgets
        self.lineEditStudentID = QLineEdit(self)
        self.lineEditFullName = QLineEdit(self)
        self.lineEditAddress = QLineEdit(self)
        self.lineEditPhone = QLineEdit(self)
        self.lineEditEmail = QLineEdit(self)
        self.lblStudentImg = QLabel(self)
        self.btnSexMale = QPushButton("Male")
        self.btnSexFemale = QPushButton("Female")
        self.btnSexOthers = QPushButton("Prefer Not To Say")

        # Widget Properties
        self.grid.setSpacing(10)
        self.pixMap = QPixmap('img/profile.png')
        self.lblStudentImg.setPixmap(self.pixMap.scaled(100, 200, Qt.KeepAspectRatio))
        self.lblStudentImg.setCursor(Qt.PointingHandCursor)
        self.lblStudentImg.setAlignment(Qt.AlignCenter)
        self.lblStudentImg.setFixedHeight(200)
        self.lineEditStudentID.setFixedWidth(500)
        self.btnSexMale.setCursor(Qt.PointingHandCursor)
        self.btnSexFemale.setCursor(Qt.PointingHandCursor)
        self.btnSexOthers.setCursor(Qt.PointingHandCursor)

        # Add to Main Layout

        # Add to SubLayout
        self.hBoxGenderLayout.addWidget(self.btnSexMale)
        self.hBoxGenderLayout.addWidget(self.btnSexFemale)
        self.hBoxGenderLayout.addWidget(self.btnSexOthers)

        # Add to Grid Layout Student Details
        self.grid.addWidget(self.lblStudentImg)
        self.grid.addWidget(QLabel("Student ID"))
        self.grid.addWidget(self.lineEditStudentID)
        self.grid.addWidget(QLabel("Full Name"))
        self.grid.addWidget(self.lineEditFullName)
        self.grid.addWidget(QLabel("Gender"))
        self.grid.addLayout(self.hBoxGenderLayout)
        self.grid.addWidget(QLabel("Address"))
        self.grid.addWidget(self.lineEditAddress)
        self.grid.addWidget(QLabel("Phone"))
        self.grid.addWidget(self.lineEditPhone)
        self.grid.addWidget(QLabel("Email"))
        self.grid.addWidget(self.lineEditEmail)

        # Listeners
        self.btnSexMale.clicked.connect(self.genderSelectButtonClicked)
        self.btnSexFemale.clicked.connect(self.genderSelectButtonClicked)
        self.btnSexOthers.clicked.connect(self.genderSelectButtonClicked)

        # Add to main layout
        self.setLayout(self.grid)

        # Global Variable
        self.gender = ''

        self.setCSS()

    def setCSS(self):
        css = '''
        QLabel {
            color: white;
            font-size: 15px;
            margin-top: 20px;
        }
        QLineEdit {
            font-size: 20px;
            height: 30px;
            border-width: 2px; 
            border-style: solid; 
            border-color: ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_HERB + ''' ''' + cfg.COLOR_CHARCOAL + ''' ;
            color: ''' + cfg.COLOR_HERB + ''';
        }
        QLineEdit:focus {
            border: 2px solid #006080;
            border-color: ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHILI + ''' ''' + cfg.COLOR_CHARCOAL + ''' ;
            color: ''' + cfg.COLOR_CHILI + ''';
        }
        QPushButton {
            padding: 15px;
            color: white;
            border-width: 2px; 
            border-style: solid; 
            border-color: ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_HERB + ''' ''' + cfg.COLOR_CHARCOAL + ''' ;
            color: ''' + cfg.COLOR_HERB + ''';
        }
        QPushButton:hover {
            color: red;
        }
        '''
        self.setStyleSheet(css)
        self.grid.setAlignment(Qt.AlignTop)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def genderSelectButtonClicked(self):
        selectedCSS = '''
                border-color: ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHILI + ''' ''' + cfg.COLOR_CHARCOAL + ''' ;
                color: ''' + cfg.COLOR_CHILI + ''';
                font-weight: bold;
            '''
        defaultCSS = '''
                border-color: ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_CHARCOAL + ''' ''' + cfg.COLOR_HERB + ''' ''' + cfg.COLOR_CHARCOAL + ''' ;
                color: ''' + cfg.COLOR_HERB + ''';
            '''
        btn = self.sender()
        self.gender = btn.text()
        if btn.text() == 'Male':
            self.btnSexMale.setStyleSheet(selectedCSS)
            self.btnSexFemale.setStyleSheet(defaultCSS)
            self.btnSexOthers.setStyleSheet(defaultCSS)
        elif btn.text() == 'Female':
            self.btnSexMale.setStyleSheet(defaultCSS)
            self.btnSexFemale.setStyleSheet(selectedCSS)
            self.btnSexOthers.setStyleSheet(defaultCSS)
        elif btn.text() == 'Prefer Not To Say':
            self.btnSexMale.setStyleSheet(defaultCSS)
            self.btnSexFemale.setStyleSheet(defaultCSS)
            self.btnSexOthers.setStyleSheet(selectedCSS)
