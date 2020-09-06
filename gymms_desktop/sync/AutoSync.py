from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, time, os

from CustomMessageBox import *
import Configuration as cfg
import sync.FBAutoSync as FBAutoSync
import sync.SQLAutoSync as SQLAutoSync
import sync.CompareStudentsData as CompareStudentsData
import home.SQLTabHome as SQLTabHome


class AutoSync(QDialog):
    def __init__(self):
        super(AutoSync, self).__init__()
        self.phone = ''
        self.done = False
        self.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        self.setWindowTitle("Syncing Data...")
        self.setMinimumWidth(500)
        # self.closeEvent = self.closeDialogEvent

        # Layouts
        self.mainLayout = QGridLayout()

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.lblInProgress = QLabel("Fetching data...")
        self.progress = QProgressBar()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout

        # Add to Main Layout
        self.mainLayout.addWidget(self.lblInProgress, 0, 0)
        self.mainLayout.addWidget(self.progress, 1, 0)

        # Add Main Widget to Parent Layout
        self.setLayout(self.mainLayout)

        self.startSync()

    def setLayoutProperties(self):
        pass

    def setSubLayoutProperties(self):
        pass

    def setWidgetProperties(self):
        pass

    def setListeners(self):
        pass

    # Override :: Stop dialog close till the database is being updated
    def closeEvent(self, event):
        if not self.done:
            event.ignore()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
            msg.setWindowTitle("Error")
            msg.setText("Please wait while we index your database.")
            msg.exec_()
        else:
            self.close()

    # Override :: Stop dialog close when escape is clicked
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if not self.done:
                event.ignore()
                msg = CustomInfoMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Error")
                msg.setText("Please wait while we index your database.")
                msg.exec_()
            else:
                self.close()

    def connectedToInternet(self):
        # url = 'https://jsonplaceholder.typicode.com/todos/1'
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)

        return res.status_code

    def startSync(self):
        if self.connectedToInternet() != 200:

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
            msg.setWindowTitle("Error")
            msg.setText("Please connect to the internet and try again!")
            msg.exec_()

        self.startProgress()

    def startProgress(self):
        self.thread = ThreadProgressBarShow()
        self.thread.change_val.connect(self.setProgressValue)
        self.thread.thread_done.connect(self.setDone)
        self.thread.lbl_msg.connect(self.setLabelMsg)
        self.thread.start()

    def setProgressValue(self, val):
        self.progress.setValue(val)

    def setDone(self, done):
        self.done = done
        if done:
            self.done = True
            # msg = CustomInfoMessageBox()
            # msg.setWindowTitle('Done')
            # msg.setText('Your sync process is complete!')
            # msg.exec_()
            self.close()

    def setLabelMsg(self, msg):
        self.lblInProgress.setText(msg)


class ThreadProgressBarShow(QThread):
    change_val = pyqtSignal(int)
    thread_done = pyqtSignal(bool)
    lbl_msg = pyqtSignal(str)

    fb = FBAutoSync.FBAutoSync()
    sql = SQLAutoSync.SQLAutoSync()

    def run(self):
        students = {}
        notifs = {}
        attend = {}
        sql = SQLTabHome.SQLTabHome()
        gymid = sql.getGymId()
        del sql

        sql = SQLAutoSync.SQLAutoSync()

        fb = FBAutoSync.FBAutoSync()

        if self.isConnectedToInternet() == 200:
            students = fb.getAllStudentsData(gymid)
        else:
            return

        if self.isConnectedToInternet() == 200:
            notifs = fb.getAllNotificationData(gymid)
        else:
            return

        if self.isConnectedToInternet() == 200:
            attend = fb.getAllAttendenceData(gymid)
        else:
            return

        totalDateCount = len(students) + len(notifs) + len(attend)

        if totalDateCount != 0:
            self.lbl_msg.emit("Syncing Students...")
            if students.__len__() != 0:
                sql.insertStudents(students)
            self.change_val.emit(30)

            self.lbl_msg.emit("Syncing Notifications...")
            if notifs.__len__() != 0:
                sql.insertNotifications(notifs)

            self.change_val.emit(60)

            self.lbl_msg.emit("Syncing Attendance...")
            if attend.__len__() != 0:
                for sid in attend.keys():
                    dates = attend[sid]
                    sql.insertAttendence(sid, dates)

        self.change_val.emit(90)
        self.lbl_msg.emit("Done.")
        sql.updateSoftwareFirstInstallFlag(cfg.CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS, "1")

        self.change_val.emit(100)
        self.thread_done.emit(True)

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code