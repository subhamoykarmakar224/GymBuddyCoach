from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg


class TabStudent(QWidget):
    def __init__(self):
        super(TabStudent, self).__init__()

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.layoutSearch = QHBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblStudents = QLabel("Students List")
        self.lineEdtSearch = QLineEdit()
        self.lblClearIcon = QLabel()
        self.pixMapICClear = QPixmap(cfg.IC_DELETE)
        self.tableStudentsList = QTableWidget()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.layoutSearch.addWidget(self.lineEdtSearch)
        self.layoutSearch.addWidget(self.lblClearIcon)

        # Add to Main Layout
        self.mainLayout.addWidget(self.lblStudents, 0, 0)
        self.mainLayout.addLayout(self.layoutSearch, 1, 0)
        self.mainLayout.addWidget(self.tableStudentsList, 2, 0)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        # Search LineEdit
        self.lineEdtSearch.setPlaceholderText("Search...")
        self.lblClearIcon.setPixmap(self.pixMapICClear.scaled(15, 15, Qt.KeepAspectRatio))
        self.lblClearIcon.setCursor(Qt.PointingHandCursor)
        self.lblClearIcon.setToolTip("Clear Search Term")

        # Student List table
        self.tableStudentsList.setColumnCount(3)
        self.tableStudentsList.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Membership']
        )
        self.tableStudentsList.horizontalHeader().setStretchLastSection(True)
        self.tableStudentsList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableStudentsList.setColumnWidth(0, 70)
        self.tableStudentsList.setColumnWidth(1, 400)

    def setListeners(self):
        pass