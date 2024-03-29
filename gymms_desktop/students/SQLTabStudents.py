import mysql.connector as mysql
import Configuration as cfg
import requests, uuid


class SQLTabStudents:
    def __init__(self):
        self.db = mysql.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            passwd=cfg.db_passwd,
            db=cfg.db_gymms
        )
        self.cur = self.db.cursor()

    # Get all students
    def getAllStudents(self):
        query = 'select * from ' + cfg.TABLE_STUDENTS
        res = []
        try:
            self.cur.execute(query)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabStudents.getAllStudents() :: ERROR :: " + str(e))

        return res

    # Get count of students in sql
    def getStudentsCount(self):
        query ='select count(*) from ' + cfg.TABLE_STUDENTS
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res

    # insert students to SQL
    def insertStudents(self, students):
        try:
            for s in students:
                q = 'insert into ' + cfg.TABLE_STUDENTS + \
                    ' (' + cfg.KEY_STUDENTS_SID + ', ' + cfg.KEY_STUDENTS_ALLOTTED_TIME + ', ' + \
                    cfg.KEY_STUDENTS_MEMBERSHIP + ', ' + cfg.KEY_STUDENTS_PHONE + ', ' + \
                    cfg.KEY_STUDENTS_AGE + ', ' + cfg.KEY_STUDENTS_NAME + ', ' + \
                    cfg.KEY_STUDENTS_REG_STATUS + ', ' + cfg.KEY_STUDENTS_DUE + ') values ("'+ \
                    s[cfg.FB_KEY_STUDENTS_SID] + '", "'+ s[cfg.FB_KEY_STUDENTS_ALLOTTED_TIME] + '", "'+ \
                    s[cfg.FB_KEY_STUDENTS_MEMBERSHIP] + '", "'+ s[cfg.FB_KEY_STUDENTS_PHONE] + '", "'+ \
                    s[cfg.FB_KEY_STUDENTS_AGE] + '", "'+ s[cfg.FB_KEY_STUDENTS_NAME] + '", "'+ \
                    s[cfg.FB_KEY_STUDENTS_REG_STATUS] + '", "'+ s[cfg.DB_KEY_STUDENTS_DUE] + '")'
                self.cur.execute(q)
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR1 :: " + str(e))
            return -1

        try:
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR2 :: " + str(e))
            return -1
        return 0

    # insert students to SQL
    def insertStudentsAlternate(self, students):
        try:
            for st in students:
                s = students[st]
                q = 'insert into ' + cfg.TABLE_STUDENTS + \
                    ' (' + cfg.KEY_STUDENTS_SID + ', ' + cfg.KEY_STUDENTS_ALLOTTED_TIME + ', ' + \
                    cfg.KEY_STUDENTS_MEMBERSHIP + ', ' + cfg.KEY_STUDENTS_PHONE + ', ' + \
                    cfg.KEY_STUDENTS_AGE + ', ' + cfg.KEY_STUDENTS_NAME + ', ' + \
                    cfg.KEY_STUDENTS_REG_STATUS + ', ' + cfg.KEY_STUDENTS_DUE + ') values ("' + \
                    s[cfg.FB_KEY_STUDENTS_SID] + '", "' + s[cfg.FB_KEY_STUDENTS_ALLOTTED_TIME] + '", "' + \
                    s[cfg.FB_KEY_STUDENTS_MEMBERSHIP] + '", "' + s[cfg.FB_KEY_STUDENTS_PHONE] + '", "' + \
                    s[cfg.FB_KEY_STUDENTS_AGE] + '", "' + s[cfg.FB_KEY_STUDENTS_NAME] + '", "' + \
                    s[cfg.FB_KEY_STUDENTS_REG_STATUS] + '", "' + s[cfg.DB_KEY_STUDENTS_DUE] + '")'
                self.cur.execute(q)
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR1 :: " + str(e))
            return -1

        try:
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR2 :: " + str(e))
            return -1
        return 0

    def updateStudentInfo(self, student):
        q = 'update ' + cfg.TABLE_STUDENTS + \
            ' set ' + cfg.KEY_STUDENTS_ALLOTTED_TIME + '="'+ student[cfg.KEY_STUDENTS_ALLOTTED_TIME] +'", ' + \
            cfg.KEY_STUDENTS_MEMBERSHIP + '="'+ student[cfg.KEY_STUDENTS_MEMBERSHIP] +'", ' + cfg.KEY_STUDENTS_PHONE + '="'+ student[cfg.KEY_STUDENTS_PHONE] +'", ' + \
            cfg.KEY_STUDENTS_AGE + '="'+ student[cfg.KEY_STUDENTS_AGE] +'", ' + cfg.KEY_STUDENTS_NAME + '="'+ student[cfg.KEY_STUDENTS_NAME] +'", ' + \
            cfg.KEY_STUDENTS_REG_STATUS + '="'+ student[cfg.KEY_STUDENTS_REG_STATUS] +'", ' + cfg.KEY_STUDENTS_DUE + '="'+ student[cfg.KEY_STUDENTS_DUE] +'" where ' + cfg.KEY_STUDENTS_SID + '="' + \
            student[cfg.KEY_STUDENTS_SID] + '"'
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLAutoSync.updateStudentInfo() :: ERROR1 :: " + str(e))
            return -1

        try:
            pass
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR2 :: " + str(e))
            return -1
        return 0

    def updateStudentMembershipInfo(self, student):
        q = 'update ' + cfg.TABLE_STUDENTS + \
            ' set ' + cfg.KEY_STUDENTS_MEMBERSHIP + '="' + student[cfg.KEY_STUDENTS_MEMBERSHIP] + '", ' + \
            cfg.KEY_STUDENTS_REG_STATUS + '="' + student[cfg.KEY_STUDENTS_REG_STATUS] + '", ' + \
            cfg.KEY_STUDENTS_DUE + '="' + student[cfg.KEY_STUDENTS_DUE] + '" where ' + cfg.KEY_STUDENTS_SID + '="' + \
            student[cfg.KEY_STUDENTS_SID] +'"'

        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLAutoSync.updateStudentMembershipInfo() :: ERROR1 :: " + str(e))
            return -1

        try:
            pass
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR2 :: " + str(e))
            return -1
        return 0

    def getLocalActionStudentModule(self):
        query = 'select ' + cfg.KEY_ACTION_ACTION + ' from ' + cfg.TABLE_ACTION + ' where module="student" and status=0'
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res

    # Get the GYM id
    def getGymId(self):
        query = 'select ' + cfg.KEY_ADMIN_ID + ' from ' + cfg.TABLE_ADMIN
        res = ""
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res[0]

    # Checks if the phone number os already present in the DB
    def studentPhoneAlreadyPresentStatus(self, ph):
        q = 'select count(*) from ' + cfg.TABLE_STUDENTS + ' where ' + cfg.KEY_STUDENTS_PHONE + '="' + ph + '"'
        res = 0
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLAutoSync.studentPhoneAlreadyPresentStatus() :: ERROR :: " + str(e))

        return res

    # Checks if the phone number os already present in the DB
    def studentPhoneAlreadyPresentStatusExcept(self, ph, sid):
        q = 'select count(*) from ' + cfg.TABLE_STUDENTS + ' where ' + cfg.KEY_STUDENTS_PHONE + '="' + ph + '" and ' + \
            cfg.KEY_STUDENTS_SID + '!="' + sid + '"'
        res = 0
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLAutoSync.studentPhoneAlreadyPresentStatus() :: ERROR :: " + str(e))

        return res

    # delete the student from database as per SID
    def deleteStudent(self, id):
        q = 'delete from ' + cfg.TABLE_STUDENTS + ' where ' + cfg.KEY_STUDENTS_SID + '="' + str(id) + '"'
        try:
            self.cur.execute(q)
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.studentPhoneAlreadyPresentStatus() :: ERROR :: " + str(e))
            return 0

        return 1

    # Get Student information as per student id
    def getStudentInfo(self, sid):
        q = 'select * from ' + cfg.TABLE_STUDENTS + ' where ' + cfg.KEY_STUDENTS_SID + '="' + str(sid) + '"'
        res = {}
        tmp = ()
        try:
            self.cur.execute(q)
            tmp = self.cur.fetchone()
        except Exception as e:
            print("SQLAutoSync.studentPhoneAlreadyPresentStatus() :: ERROR :: " + str(e))
            return res

        if tmp != ():
            res[cfg.KEY_STUDENTS_SID] = tmp[0]
            res[cfg.KEY_STUDENTS_ALLOTTED_TIME] = tmp[1]
            res[cfg.KEY_STUDENTS_MEMBERSHIP] = tmp[2]
            res[cfg.KEY_STUDENTS_PHONE] = tmp[3]
            res[cfg.KEY_STUDENTS_AGE] = tmp[4]
            res[cfg.KEY_STUDENTS_NAME] = tmp[5]
            res[cfg.KEY_STUDENTS_REG_STATUS] = tmp[6]
            res[cfg.KEY_STUDENTS_DUE] = tmp[7]

        return res

    # Gets Last Notification Cnt
    def getLastNotificationMsgCnt(self):
        q = 'select ' + cfg.KEY_MSG_NOTIF_CNT + ' from ' + cfg.TABLE_MSG_NOTIF + ' order by ' + \
            cfg.KEY_MSG_NOTIF_CNT + ' desc limit 1'
        tmp = 0
        try:
            self.cur.execute(q)
            tmp = self.cur.fetchone()
        except Exception as e:
            print("SQLAutoSync.getLastNotificationCnt() :: ERROR :: " + str(e))
            return tmp

        if tmp is None:
            tmp = (0,)

        return tmp

    def sendNotificationsMsg(self, sids, msg):
        startIndex = self.getLastNotificationMsgCnt()[0]
        startIndex += 1
        for sid in sids:
            q = 'insert into ' + cfg.TABLE_MSG_NOTIF + ' (' + cfg.KEY_MSG_NOTIF_CNT + ', ' + \
                cfg.KEY_MSG_NOTIF_SID + ', ' + cfg.KEY_MSG_NOTIF_MSG + ') values ('+str(startIndex)+',"' + sid[0] + '", "' + msg + '")'
            startIndex += 1
            try:
                self.cur.execute(q)
            except Exception as e:
                print("SQLAutoSync.sendNotificationsMsg() :: ERROR :: " + str(e))
                return 0

            try:
                self.db.commit()
            except Exception as e:
                print("SQLAutoSync.sendNotifications() :: ERROR :: " + str(e))
                return 0
        return 1

    def sendNewNotification(self, gymId, sid, level, msg):
        if self.isConnectedToInternet() != 200:
            pass

    def getCheckedInStatus(self, sid, d):
        q = 'select count(*) from ' + cfg.TABLE_ATTENDENCE + ' where ' + \
            cfg.KEY_ATTENDENCE_SID + '="' + sid + '" and ' + cfg.KEY_ATTENDENCE_DATE + '=STR_TO_DATE("' + \
            d + '", "%d-%m-%Y")'
        res = 0
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

        return res[0]

    def getAllCustomMessage(self):
        q = 'select *from ' + cfg.TABLE_CUSTOM_MESSAGE
        res = []
        try:
            self.cur.execute(q)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

        return res

    def searchTermQuery(self, term):
        month = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
            'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
            'November': '11', 'December': '12'
        }

        q = 'select * from ' + cfg.TABLE_STUDENTS + ' where ' + cfg.KEY_STUDENTS_SID + ' like "%' + term + '%" or ' + \
            cfg.KEY_STUDENTS_NAME + ' like "%' + term + '%"'
        res = []
        try:
            self.cur.execute(q)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabStudents.getAllStudents() :: ERROR :: " + str(e))

        return res

    def getAttendanceForAMonth(self, sid, month, year, lastDate):
        d1 = year + '-' + month + '-01'
        d2 = year + '-' + month + '-' + lastDate
        q = 'select * from ' + cfg.TABLE_ATTENDENCE + ' where SID="' + sid + \
            '" and datestamp like "' + year + '-' + month + '-%" order by datestamp asc'
        res = []
        try:
            self.cur.execute(q)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabStudents.getAttendanceForAMonth() :: ERROR :: " + str(e))

        return res

    def getFirstInstallFlagStudent(self):
        q = 'select ' + cfg.KEY_SOFTWARE_FLAG_STATUS + ' from ' + cfg.TABLE_SOFTWARE_FLAG + ' where ' + \
            cfg.KEY_SOFTWARE_FLAG_NAME + '="' + cfg.CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS + '"'
        res = 0
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

        return str(res[0])

    def updateFirstInstallFlagStudent(self):
        q = 'update ' + cfg.TABLE_SOFTWARE_FLAG + ' set ' + cfg.KEY_SOFTWARE_FLAG_STATUS + '="1" where ' + \
            cfg.KEY_SOFTWARE_FLAG_NAME + '="' + cfg.CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS + '"'
        res = 0
        try:
            self.cur.execute(q)
            self.db.commit()
        except Exception as e:
            print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code

