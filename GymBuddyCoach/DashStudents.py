from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configuration as cfg
import StudentView as studentgrid


# Student Dash
class DashStudents(QWidget):
    def __init__(self):
        super(DashStudents, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main Layout
        hBoxLayout = QHBoxLayout(self)

        # Sub Layout
        self.vBoxStudent = QGridLayout(self)

        # Widgets
        self.lineEditSearch = QLineEdit(self)
        self.tableStudents = QTableWidget(self)

        # Widget Properties
        self.lineEditSearch.setStyleSheet('''
            background: #f3f3f3;
            background-image: url(img/search.svg);
            background-repeat: no-repeat;
            background-position: left;
            color: #252424;
            font-family: SegoeUI;
            font-size: 12px;
            padding: 2 5 2 25;
            height: 30px;
            background-color: white; 
            height: 30px; 
            font-size: 15px;
        ''')
        self.tableStudents.setColumnCount(2)
        self.tableStudents.setHorizontalHeaderLabels(['ID', 'Student'])
        self.tableStudents.horizontalHeader().setStretchLastSection(True)
        self.tableStudents.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableStudents.setColumnWidth(0, 100)
        self.tableStudents.setRowCount(100)
        self.tableStudents.setMinimumWidth(400)
        self.tableStudents.setMaximumWidth(400)
        self.tableStudents.setStyleSheet("background-color: white;")

        # Add to Main Layout

        # Add to Grid Layout Student Details


        # Listeners

        # Add to SubLayout
        self.vBoxStudent.addWidget(self.lineEditSearch)
        self.vBoxStudent.addWidget(self.tableStudents)

        # Add to main layout
        hBoxLayout.addLayout(self.vBoxStudent)
        hBoxLayout.addWidget(studentgrid.StudentView(""))

        # Add to main layout
        self.setLayout(hBoxLayout)
