from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import sys
import mysql.connector as mysql

import MainWindow as mw
import Configuration as cfg
import GYMMSSystemTray as CustomSystemTray
import EnterCDKey as EnterCDKey


def startAPP():
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(cfg.TITLEBAR_ICON_URL))
    trayIcon = CustomSystemTray.GYMMSSystemTray(app)
    trayIcon.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='PyQt5'))

    cdKeyIsPresent = getCDKeyIsPresent()
    if cdKeyIsPresent == 0:
        cdkey_dialog = EnterCDKey.EnterCDKey()
        cdkey_dialog.exec_()

        if not cdkey_dialog.allOK:
            sys.exit(0)
        else:
            mw.MainWindowApplication(trayIcon)
    elif cdKeyIsPresent == 1:
        mw.MainWindowApplication(trayIcon)

    sys.exit(app.exec_())


# Checks if CD Key already present
def getCDKeyIsPresent():
    db = mysql.connect(
        host=cfg.db_host,
        user=cfg.db_user,
        passwd=cfg.db_passwd,
        db=cfg.db_gymms
    )
    cur = db.cursor()
    q = 'select count(*) from ' + cfg.TABLE_CDKEY
    res = 0
    try:
        cur.execute(q)
        res = cur.fetchone()[0]
    except Exception as e:
        print("EnterCDKey.getCDKeyIsPresent() :: ERROR :: " + str(e))

    return res