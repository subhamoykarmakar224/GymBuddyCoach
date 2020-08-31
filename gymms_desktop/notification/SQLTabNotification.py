import mysql.connector as mysql
import Configuration as cfg
import requests, uuid
import notification.FBTabNotification as FBTabNotification


class SQLTabNotification:
    def __init__(self):
        self.db = mysql.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            passwd=cfg.db_passwd,
            db=cfg.db_gymms
        )
        self.cur = self.db.cursor()

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

    # Get all notifications
    def getAllNotificationsFromToday(self, d):
        if d == '':
            query = 'select * from ' + cfg.TABLE_NOTIFICATION + ' where ' + cfg.KEY_NOTIFICATION_DATE + \
                    '=curdate() order by ' + cfg.KEY_NOTIFICATION_TIME + ' desc '
        else:
            query = 'select * from ' + cfg.TABLE_NOTIFICATION + ' where ' + cfg.KEY_NOTIFICATION_DATE + \
                    '=STR_TO_DATE("' + d + '", "%d-%m-%Y") order by ' + cfg.KEY_NOTIFICATION_TIME + ' desc '

        res = []
        try:
            self.cur.execute(query)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabNotification.getAllNotifications() :: ERROR :: " + str(e))

        return res

    # insert notifications to SQL
    def insertNotifications(self, id, n):
        if self.getIsNotificationPresent(id)[0] >= 1:
            return

        tmpdate, tmptime = self.convertToCustomDateTimeFormat(n['dateTime'])
        try:
            q = '''
            insert into notification values(
            "''' + id + '''", 
            "''' + n['studentId'] + '''", 
            "''' + n['dateTime'] + '''", 
            STR_TO_DATE("''' + tmpdate + '''", '%d-%m-%Y'), 
            "''' + tmptime + '''", 
            "''' + n['level'] + '''", 
            "''' + n['msg'] + '''"
            )
            '''
            self.cur.execute(q)
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR1 :: " + str(e))
            return -1

        try:
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.insertStudents() :: ERROR2 :: " + str(e))
            return -1

        if n['level'] == 'GREEN':
            self.insertAttendence(n['studentId'], tmpdate, tmptime)

        return 0

    def insertAttendence(self, sid, d, t):
        if self.getIsAttendencePresent(sid, d, t)[0] >= 1:
            return

        q = 'insert into ' + cfg.TABLE_ATTENDENCE + ' values ("'+sid+'", STR_TO_DATE("' + \
            d + '", "%d-%m-%Y"), "' + t + '", "0")'
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLAutoSync.insertAttendence() :: ERROR1 :: " + str(e))
            return -1

        try:
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.insertAttendence() :: ERROR2 :: " + str(e))
            return -1

        if self.isConnectedToInternet() == 200:
            res = FBTabNotification.insertAttendence(self.getGymId(), sid, d, t)
            if res != 0:
                self.updateAttendenceUploadStatus(sid, d, t)

        return 0

    def getIsAttendencePresent(self, sid, d, t):
        q = 'select count(*) from ' + cfg.TABLE_ATTENDENCE + ' where ' + \
            cfg.KEY_ATTENDENCE_SID + '="' + sid + '" and ' + cfg.KEY_ATTENDENCE_DATE + '=STR_TO_DATE("' + \
            d + '", "%d-%m-%Y") and ' + cfg.KEY_ATTENDENCE_TIME + '="' + t + '"'
        res = 0
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

        return res

    def updateAttendenceUploadStatus(self, sid, d, t):
        q = 'update ' + cfg.TABLE_ATTENDENCE + ' set ' + cfg.KEY_ATTENDENCE_UPLOAD_STATUS + '="1" where ' + \
            cfg.KEY_ATTENDENCE_SID + '="' + sid + '" and ' + cfg.KEY_ATTENDENCE_DATE + '=STR_TO_DATE("' + \
            d + '", "%d-%m-%Y") and ' + cfg.KEY_ATTENDENCE_TIME + '="' + t + '"'
        res = 1
        try:
            self.cur.execute(q)
        except Exception as e:
            print("SQLTabNotification.updateAttendenceUploadStatus() :: ERROR :: " + str(e))

        try:
            self.db.commit()
        except Exception as e:
            print("SQLAutoSync.updateAttendenceUploadStatus() :: ERROR2 :: " + str(e))
            return -1

        return res

    # Control Async upload of attendence
    def getAttendenceNotUploadedForUpload(self):
        q = 'select distinct ' + cfg.KEY_ATTENDENCE_SID + ' from ' + cfg.TABLE_ATTENDENCE + \
            ' where ' + cfg.KEY_ATTENDENCE_UPLOAD_STATUS + '="0"'
        sids = []
        try:
            self.cur.execute(q)
            sids = self.cur.fetchall()
        except Exception as e:
            print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

        if len(sids) == 0:
            return

        for s in sids:
            sid = s[0]
            data = []
            q = 'select * from ' + cfg.TABLE_ATTENDENCE + ' where ' + cfg.KEY_ATTENDENCE_SID + '="'+sid+'" and ' + \
                cfg.KEY_ATTENDENCE_UPLOAD_STATUS + '="0"'
            try:
                self.cur.execute(q)
                data = self.cur.fetchall()
            except Exception as e:
                print("SQLTabNotification.getIsAttendencePresent() :: ERROR :: " + str(e))

            for d in data: # ('ID-2932-7e24dabd', datetime.date(2020, 8, 19), datetime.timedelta(seconds=65096), '0')
                tmpDate = str(d[1]).split('-')[::-1]
                tmpDate = '-'.join(tmpDate)
                if self.isConnectedToInternet() == 200:
                    res = FBTabNotification.insertAttendence(self.getGymId(), sid, tmpDate, str(d[2]))
                    if res != 0:
                        self.updateAttendenceUploadStatus(d[0], tmpDate, str(d[2]))

    # Tue Aug 04 19:16:38 GMT+05:30 2020
    def convertToCustomDateTimeFormat(self, d):
        resDate = ''
        d = d.split(" ")
        months = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        resDate = d[2] + "-" + months[d[1]] + "-" + d[-1]
        return resDate, d[3]

    def getFilteredNotification(self, data): # d, starttime, endtime, level, searchtext
        if str(data[3]).lower().__eq__('all'):
            q = '''
            select * from ''' + cfg.TABLE_NOTIFICATION+ ''' where ''' + \
                cfg.KEY_NOTIFICATION_DATE + '''=STR_TO_DATE("''' + data[0] + '''", "%d-%m-%Y") and ''' + \
                cfg.KEY_NOTIFICATION_TIME + '''>= TIME("''' + data[1] + '''") and ''' + \
                cfg.KEY_NOTIFICATION_TIME + '''<= TIME("''' + data[2] + '''") and ''' + \
                cfg.KEY_NOTIFICATION_SID + ''' like"%''' + data[4] + '''%"'''
        else:
            q = '''
            select * from ''' + cfg.TABLE_NOTIFICATION + ''' where ''' + \
                cfg.KEY_NOTIFICATION_DATE + '''=STR_TO_DATE("''' + data[0] + '''", "%d-%m-%Y") and ''' + \
                cfg.KEY_NOTIFICATION_TIME + '''>= TIME("''' + data[1] + '''") and ''' + \
                cfg.KEY_NOTIFICATION_TIME + '''<= TIME("''' + data[2] + '''") and ''' + \
                cfg.KEY_NOTIFICATION_LEVEL + '''=upper("''' + data[3] + '''") and ''' + \
                cfg.KEY_NOTIFICATION_SID + ''' like"%''' + data[4] + '''%"'''
        res = []
        try:
            self.cur.execute(q)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabNotification.getAllNotifications() :: ERROR :: " + str(e))

        return res

    # get student name as per student ID
    def getStudentName(self, id):
        q = 'select ' + cfg.KEY_STUDENTS_NAME + ' from ' + cfg.TABLE_STUDENTS + \
            ' where ' + cfg.KEY_STUDENTS_SID + '="' + id + '"'
        res = ""
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getGymId() :: ERROR :: " + str(e))
        if res == "" or res is None:
            return "-Unknown-"
        return res[0]

    def getAllNotificationCount(self):
        q = 'select count(*) from ' + cfg.TABLE_NOTIFICATION
        res = ""
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getAllNotificationCount() :: ERROR :: " + str(e))

        return res

    def getIsNotificationPresent(self, notifID):
        q = 'select count(*) from ' + cfg.TABLE_NOTIFICATION + ' where ' + \
            cfg.KEY_NOTIFICATION_NID + '="' + notifID + '"'
        res = 0
        try:
            self.cur.execute(q)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLTabNotification.getAllNotificationCount() :: ERROR :: " + str(e))

        return res

    def deleteNotificationOlderThan15Days(self):
        q = 'select ' + cfg.KEY_NOTIFICATION_NID + ' from ' + cfg.TABLE_NOTIFICATION + \
            ' where ' + cfg.KEY_NOTIFICATION_DATE + ' < now() - interval 15 DAY'
        res = []
        gymid = self.getGymId()
        try:
            self.cur.execute(q)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLTabNotification.getAllNotifications() :: ERROR :: " + str(e))

        if len(res) == 0:
            return

        for r in res:
            notifId = r[0]
            if self.isConnectedToInternet() != 200:
                return
            r = FBTabNotification.deleteNotification(gymid, notifId)
            if r == 1:
                q = 'delete from ' + cfg.TABLE_NOTIFICATION + \
                    ' where ' +cfg.KEY_NOTIFICATION_NID + '="'+notifId+'"'
                try:
                    self.cur.execute(q)
                except Exception as e:
                    print("SQLTabNotification.getAllNotifications() :: ERROR :: " + str(e))
                try:
                    self.db.commit()
                except Exception as e:
                    print("SQLTabNotification.getAllNotifications() :: ERROR :: " + str(e))

    # check if connected to the internet
    def isConnectedToInternet(self):
        url = 'https://www.google.com/'
        try:
            res = requests.get(url, verify=False, timeout=10)
        except Exception as e:
            return str(e)
        return res.status_code

