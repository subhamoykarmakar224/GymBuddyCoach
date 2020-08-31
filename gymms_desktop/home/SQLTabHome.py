import mysql.connector as mysql
import Configuration as cfg
import requests, uuid


class SQLTabHome:
    def __init__(self):
        self.db = mysql.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            passwd=cfg.db_passwd,
            db=cfg.db_gymms
        )
        self.cur = self.db.cursor()

    # Get Gym admin full information
    def getGymAdminInfo(self, phone):
        query = 'select * from ' + cfg.TABLE_ADMIN + ' where ' + cfg.KEY_ADMIN_PHONE + '="' + phone + '"'
        res = {}
        tmp = ()
        try:
            self.cur.execute(query)
            tmp = self.cur.fetchone()
        except Exception as e:
            print("SQLTabStudents.getAllStudents() :: ERROR :: " + str(e))

        if tmp != ():
            res = {
                cfg.KEY_ADMIN_ID : tmp[0],
                cfg.KEY_ADMIN_GYM_NAME : tmp[2],
                cfg.KEY_ADMIN_NAME : tmp[3],
                cfg.KEY_ADMIN_PHONE : tmp[4],
                cfg.KEY_ADMIN_VALIDITY : tmp[5],
                cfg.KEY_ADMIN_USERNAME : tmp[6]
            }
        return res

    # Gets all Custom messages keys stored in local db
    def getAllCustomMessageKeys(self):
        q = 'select distinct ' + cfg.KEY_CUSTOM_MESSAGE_ID + ' from ' + cfg.TABLE_CUSTOM_MESSAGE
        res = []
        try:
            self.cur.execute(q)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabHome.getAllCustomMessageKeys() :: ERROR :: " + str(e))

        return res

    # Gets Custom messages stored in local db as per key
    def getCustomMessage(self, k):
        q = 'select ' + cfg.KEY_CUSTOM_MESSAGE + ' from ' + cfg.TABLE_CUSTOM_MESSAGE + ' where ' + \
            cfg.KEY_CUSTOM_MESSAGE_ID + '="' + k + '"'
        res = ""
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLTabHome.getCustomMessage() :: ERROR :: " + str(e))

        return res

    def insertNewCustomMsg(self, key, msg):
        q = 'insert into ' + cfg.TABLE_CUSTOM_MESSAGE + ' ('+cfg.KEY_CUSTOM_MESSAGE_ID+\
            ', '+cfg.KEY_CUSTOM_MESSAGE+' ) values ("'+key+'", "'+msg+'")'
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLTabHome.insertNewCustomMsg() :: ERROR :: " + str(e))
            return 0

        try:
            self.db.commit()
        except Exception as e:
            print("SQLTabHome.insertNewCustomMsg() :: ERROR :: " + str(e))
            return 0

        return 1

    def deleteCustomMsg(self, key):
        q = 'delete from ' + cfg.TABLE_CUSTOM_MESSAGE + ' where ' + cfg.KEY_CUSTOM_MESSAGE_ID + '="' + key + '"'
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLTabHome.deleteCustomMsg() :: ERROR :: " + str(e))
            return 0

        try:
            self.db.commit()
        except Exception as e:
            print("SQLTabHome.deleteCustomMsg() :: ERROR :: " + str(e))
            return 0

        return 1

    def updateCustomMsg(self, oldKey, newKey, msg):
        q = 'update ' + cfg.TABLE_CUSTOM_MESSAGE + ' set ' + cfg.KEY_CUSTOM_MESSAGE_ID + '="'+newKey+'" , ' + \
            cfg.KEY_CUSTOM_MESSAGE + '="'+msg+'" where ' + cfg.KEY_CUSTOM_MESSAGE_ID + '="'+ oldKey +'"'

        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLTabHome.updateCustomMsg() :: ERROR :: " + str(e))
            return 0

        try:
            self.db.commit()
        except Exception as e:
            print("SQLTabHome.updateCustomMsg() :: ERROR :: " + str(e))
            return 0

        return 1

    # Get the GYM id
    def getGymId(self):
        query = 'select ' + cfg.KEY_ADMIN_ID + ' from ' + cfg.TABLE_ADMIN
        res = ""
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getGymId() :: ERROR :: " + str(e))

        return res[0]

    def getSoftwareValidityDate(self):
        query = 'select ' + cfg.KEY_ADMIN_VALIDITY + ' from ' + cfg.TABLE_ADMIN
        res = ""
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getGymId() :: ERROR :: " + str(e))

        return res[0]

    def updateSoftwareValidityDate(self, d):
        q = 'update ' + cfg.TABLE_ADMIN + ' set ' + cfg.KEY_ADMIN_VALIDITY + '= STR_TO_DATE("' + \
            d + '", "%Y-%m-%d")'
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLTabHome.updateSoftwareValidityDate() :: ERROR1 :: " + str(e))
            return -1

        try:
            self.db.commit()
        except Exception as e:
            print("SQLTabHome.updateSoftwareValidityDate() :: ERROR2 :: " + str(e))
            return -1

    def updateCompleteAdminData(self, data):
        q = 'update ' + cfg.TABLE_ADMIN + ' set ' + cfg.KEY_ADMIN_NAME + '="' + data[cfg.KEY_ADMIN_NAME] + '", ' + \
            cfg.KEY_ADMIN_GYM_NAME + '="' + data[cfg.KEY_ADMIN_GYM_NAME] + '", ' + \
            cfg.FB_KEY_ADMIN_PASSWORD + '="' + data[cfg.KEY_ADMIN_PASSWD] + '", ' + \
            cfg.KEY_ADMIN_PHONE + '="' + data[cfg.KEY_ADMIN_PHONE] + '", ' + \
            cfg.KEY_ADMIN_USERNAME + '="' + data[cfg.KEY_ADMIN_USERNAME] + '" where username="' + data[cfg.KEY_ADMIN_USERNAME] + '"'
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLTabHome.updateSoftwareValidityDate() :: ERROR1 :: " + str(e))
            return -1

        try:
            self.db.commit()
        except Exception as e:
            print("SQLTabHome.updateSoftwareValidityDate() :: ERROR2 :: " + str(e))
            return -1

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code
