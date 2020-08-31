from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime

import Configuration as cfg
import home.SQLTabHome as SQLTabHome
from CustomMessageBox import *
from Helper import *


class CustomMessageMgmt(QGridLayout):
    def __init__(self):
        super(CustomMessageMgmt, self).__init__()

        self.customMsgKeys = []

        # Layout Properties
        self.setLayoutProperties()

        # Sub layout
        self.subLayoutButtons = QVBoxLayout()

        # Sub layout properties
        self.setSubLayoutProperties()

        # Widgets
        self.listWidgetCustomMsg = QListWidget()
        self.editTextMessage = QTextEdit()
        self.btnNewCustomMessage = QLabel()
        self.btnEditCustomMessage = QLabel()
        self.btnDeleteCustomMessage = QLabel()

        # Widget Properties
        self.setWidgetProperties()

        # Listeners
        self.setListeners()

        # Add to Sub Layout
        self.subLayoutButtons.addWidget(self.btnNewCustomMessage)
        self.subLayoutButtons.addWidget(self.btnEditCustomMessage)
        self.subLayoutButtons.addWidget(self.btnDeleteCustomMessage)

        # Add to Main Layout
        self.addWidget(QLabel('Custom Messages *(Click on custom msg key to see message)'), 0, 0, 1, 2)
        self.addWidget(self.listWidgetCustomMsg, 1, 0)
        self.addWidget(self.editTextMessage, 1, 1)
        self.addLayout(self.subLayoutButtons, 1, 2)

        self.initValues()

    def setLayoutProperties(self):
        self.setAlignment(Qt.AlignTop)

    def setSubLayoutProperties(self):
        self.subLayoutButtons.addStretch(1)
        self.subLayoutButtons.setAlignment(Qt.AlignTop)

    def setWidgetProperties(self):
        self.listWidgetCustomMsg.setFixedWidth(130)
        self.editTextMessage.setReadOnly(True)

        self.btnNewCustomMessage.setPixmap(getPixMap(cfg.IC_ADD))
        self.btnNewCustomMessage.setToolTip("New")
        self.btnNewCustomMessage.setCursor(Qt.PointingHandCursor)
        self.btnEditCustomMessage.setPixmap(getPixMap(cfg.IC_EDIT))
        self.btnEditCustomMessage.setToolTip("Edit")
        self.btnEditCustomMessage.setCursor(Qt.PointingHandCursor)
        self.btnDeleteCustomMessage.setPixmap(getPixMap(cfg.IC_DELETE_COLOR))
        self.btnDeleteCustomMessage.setToolTip("Delete")
        self.btnDeleteCustomMessage.setCursor(Qt.PointingHandCursor)

    def setListeners(self):
        self.listWidgetCustomMsg.itemClicked.connect(self.loadCustomMessage)
        self.btnNewCustomMessage.mousePressEvent = self.newCustomMsg
        self.btnEditCustomMessage.mousePressEvent = self.editCustomMsg
        self.btnDeleteCustomMessage.mousePressEvent = self.deleteCustomMsg

    def initValues(self):
        self.listWidgetCustomMsg.clear()
        self.editTextMessage.clear()
        self.customMsgKeys.clear()

        sql = SQLTabHome.SQLTabHome()
        data = sql.getAllCustomMessageKeys()
        for d in data:
            self.customMsgKeys.append(d[0])

        self.listWidgetCustomMsg.addItems(self.customMsgKeys)

    # Listener for on item  clicked in list
    def loadCustomMessage(self, e):
        self.editTextMessage.setText("")
        option = str(e.text())
        if option == '':
            return
        sql = SQLTabHome.SQLTabHome()
        msg = sql.getCustomMessage(option)
        self.editTextMessage.setText(msg)

    def deleteCustomMsg(self, e):
        if self.editTextMessage.toPlainText() == '':
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Please first select a custom message by clicking a message key from the list. "
                        "Then only you will be allowed to perform this action")
            msg.exec_()
            return
        key = self.listWidgetCustomMsg.currentItem().text()
        customMsg = self.editTextMessage.toPlainText()
        msg = CustomCriticalMessageBox()
        msg.setWindowTitle("Alert")
        msg.setText("Are you sure you want to delete the following custom message? \nMessage Key: " +
                    key + "\nMessage: " + customMsg)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.No:
            return

        msg = CustomCriticalMessageBox()
        msg.setWindowTitle("Alert")
        msg.setText("The delete operation you are about to perform is a parmanent delete operation. Are you sure you "
                    "want to proceed?")
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.No:
            return
        sql = SQLTabHome.SQLTabHome()
        res = sql.deleteCustomMsg(key)
        if res == 1:
            self.initValues()
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Done")
            msg.setText("The Custom message has been deleted!")
            msg.exec_()
        else:
            msg = CustomCriticalMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("There was an error while deleting the custom message. Please try again")
            msg.exec_()

    # Adds new Custom message to local db
    def newCustomMsg(self, e):
        key = ""
        msg = ""
        self.dialogAddNewCustomMsg = QDialog()
        self.dialogAddNewCustomMsg.setFixedSize(300, 300)
        self.dialogAddNewCustomMsg.setWindowTitle("Add New Custom Message...")
        self.dialogAddNewCustomMsg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        form = QGridLayout()

        self.editKey = QLineEdit()
        lblMsg = QLabel('Custom Message')
        self.editMsg = QTextEdit()

        btnSave = QPushButton("Save")
        btnCancel = QPushButton("Cancel")

        self.editKey.setPlaceholderText("Message Key Here...")
        lblMsg.setAlignment(Qt.AlignTop)
        self.editMsg.setPlaceholderText("Your Custom Message here...")

        form.addWidget(QLabel('Message Key'), 0, 0)
        form.addWidget(self.editKey, 0, 1, 1, 2)
        form.addWidget(lblMsg, 1, 0)
        form.addWidget(self.editMsg, 1, 1, 1, 2)
        form.addWidget(btnSave, 2, 1)
        form.addWidget(btnCancel, 2, 2)

        btnSave.clicked.connect(self.saveNewCustomMsg)
        btnCancel.clicked.connect(lambda : self.dialogAddNewCustomMsg.close())

        self.dialogAddNewCustomMsg.setLayout(form)

        self.dialogAddNewCustomMsg.exec_()

    def saveNewCustomMsg(self):
        key = self.editKey.text().__str__().strip(" ")
        msg = self.editMsg.toPlainText().__str__().strip(" ")
        if key == "":
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Custom Message cannot be left blank. Please provide a "
                        "unique key for this message")
            msg.exec_()
            return

        if self.customMsgKeys.__contains__(key):
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("A Custom Message with this name already exists. Please "
                        "enter a unique key for this message and try again.")
            msg.exec_()
            return

        if msg == "":
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Message cannot be left blank. Please enter a valid "
                        "custom message and try again")
            msg.exec_()
            return
        sql = SQLTabHome.SQLTabHome()
        r = sql.insertNewCustomMsg(key, msg)

        if r == 0:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("There was an error while inserting your custom message. Please try again.")
            msg.exec_()
            return

        del sql
        self.initValues()
        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Saved")
        msg.setText("The new Custom message has been saved.")
        r = msg.exec_()
        if r == QMessageBox.Ok:
            self.dialogAddNewCustomMsg.close()

    def editCustomMsg(self, e):
        if self.editTextMessage.toPlainText() == '':
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Please first select a custom message by clicking a message key from the list. "
                        "Then only you will be allowed to perform this action")
            msg.exec_()
            return

        self.dialogEditCustomMsg = QDialog()
        self.dialogEditCustomMsg.setFixedSize(300, 300)
        self.dialogEditCustomMsg.setWindowTitle("Add New Custom Message...")
        self.dialogEditCustomMsg.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
        form = QGridLayout()

        self.editKey = QLineEdit()
        lblMsg = QLabel('Custom Message')
        self.editMsg = QTextEdit()

        btnSave = QPushButton("Save")
        btnCancel = QPushButton("Cancel")

        self.editKey.setText(self.listWidgetCustomMsg.currentItem().text())
        lblMsg.setAlignment(Qt.AlignTop)
        self.editMsg.setPlaceholderText("Your Custom Message here...")
        self.editMsg.setText(self.editTextMessage.toPlainText().strip(" "))

        form.addWidget(QLabel('Message Key'), 0, 0)
        form.addWidget(self.editKey, 0, 1, 1, 2)
        form.addWidget(lblMsg, 1, 0)
        form.addWidget(self.editMsg, 1, 1, 1, 2)
        form.addWidget(btnSave, 2, 1)
        form.addWidget(btnCancel, 2, 2)

        btnSave.clicked.connect(self.saveEditCustomMsg)
        btnCancel.clicked.connect(lambda: self.dialogEditCustomMsg.close())

        self.dialogEditCustomMsg.setLayout(form)

        self.dialogEditCustomMsg.exec_()

    def saveEditCustomMsg(self):
        oldKey = self.listWidgetCustomMsg.currentItem().text()
        newkey = self.editKey.text().__str__().strip(" ")
        msg = self.editMsg.toPlainText().__str__().strip(" ")
        if newkey == "":
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Custom Message Key cannot be left blank. Please provide a "
                        "unique key for this message")
            msg.exec_()
            return

        if self.customMsgKeys.__contains__(newkey):
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("A Custom Message with this name already exists. Please "
                        "enter a unique key for this message and try again.")
            msg.exec_()
            return

        if msg == "":
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Message cannot be left blank. Please enter a valid "
                        "custom message and try again")
            msg.exec_()
            return

        sql = SQLTabHome.SQLTabHome()
        r = sql.updateCustomMsg(oldKey, newkey, msg)

        if r == 0:
            msg = CustomInfoMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("There was an error while updating your custom message. Please try again.")
            msg.exec_()
            return

        del sql
        self.initValues()
        msg = CustomInfoMessageBox()
        msg.setWindowTitle("Saved")
        msg.setText("The Custom message has been saved.")
        r = msg.exec_()
        if r == QMessageBox.Ok:
            self.dialogEditCustomMsg.close()
