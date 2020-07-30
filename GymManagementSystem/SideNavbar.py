from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import DashHome as home
import DashStudents as students
import DashSettings as settings


# Title Bar
class SideNavbar(QWidget):
    def __init__(self):
        super(SideNavbar, self).__init__()
        css = """
                QWidget{
                    background: """ + cfg.COLOR_CHARCOAL + """
                    color:red
                    font:12px bold
                    font-weight:bold
                    border-radius: 1px
                    height: 11px
                }
                """
        self.setAutoFillBackground(True)
        self.setStyleSheet(css)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Main Layout
        self.gridLayout = QGridLayout(self)

        # Sub Layout
        vbox = QVBoxLayout(self)

        # Widgets
        self.btnMenu = QPushButton(self)
        self.btnHome = QPushButton(self)
        self.btnStudents = QPushButton(self)
        self.btnNotification = QPushButton(self)
        self.btnSettings = QPushButton(self)

        # Widget Properties
        self.btnMenu.setIcon(QIcon('img/menu2.png'))
        self.btnMenu.setMinimumHeight(10)
        self.btnMenu.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnMenu.setToolTip("Hide/Show Menu Details")
        self.btnMenu.setCursor(Qt.PointingHandCursor)

        self.btnHome.setIcon(QIcon('img/home.png'))
        self.btnHome.setMinimumHeight(10)
        self.btnHome.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnHome.setToolTip("Home")
        self.btnHome.setCursor(Qt.PointingHandCursor)

        self.btnStudents.setIcon(QIcon('img/people.png'))
        self.btnStudents.setMinimumHeight(10)
        self.btnStudents.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnStudents.setToolTip("Students")
        self.btnStudents.setCursor(Qt.PointingHandCursor)

        self.btnNotification.setIcon(QIcon('img/ic_notification.png'))
        self.btnNotification.setMinimumHeight(10)
        self.btnNotification.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnNotification.setToolTip("Notifications")
        self.btnNotification.setCursor(Qt.PointingHandCursor)

        self.btnSettings.setIcon(QIcon('img/settings.png'))
        self.btnSettings.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnSettings.setMinimumHeight(10)
        self.btnSettings.setToolTip("Settings")
        self.btnSettings.setCursor(Qt.PointingHandCursor)

        # Add to Main Layout
        vbox.addWidget(self.btnMenu)
        vbox.addWidget(self.btnHome)
        vbox.addWidget(self.btnStudents)
        vbox.addWidget(self.btnNotification)
        vbox.addWidget(self.btnSettings)
        vbox.insertStretch(3, 100)
        vbox.setSpacing(0)

        # Listeners
        self.btnHome.clicked.connect(self.btnHomeClicked)
        self.btnStudents.clicked.connect(self.btnStudentsClicked)
        self.btnSettings.clicked.connect(self.btnSettingsClicked)

        # Add sub layouts to main layout
        self.gridLayout.addLayout(vbox, 0, 0)
        # self.gridLayout.addWidget(home.DashHome(), 0, 1)
        self.gridLayout.addWidget(students.DashStudents(), 0, 1)

        # Add to main layout
        self.setLayout(self.gridLayout)

    def btnHomeClicked(self):
        self.gridLayout.addWidget(home.DashHome(), 0, 1)

    def btnStudentsClicked(self):
        self.gridLayout.addWidget(students.DashStudents(), 0, 1)
        # self.btnStudents.setStyleSheet("background-color: red;")

    def btnSettingsClicked(self):
        self.gridLayout.addWidget(settings.DashSettings(), 0, 1)
        # self.btnSettings.setStyleSheet("background-color: red;")

