import mysql.connector as mysql
import Configuration as cfg


class SQLAutoSync():
    def __init__(self):
        self.db = mysql.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            passwd=cfg.db_passwd,
            db=cfg.db_gymms
        )
        self.cur = self.db.cursor()

    # Get the Gym ID
    def getAdminPhone(self):
        query = 'select ' + cfg.KEY_ADMIN_PHONE + ' from ' + cfg.TABLE_ADMIN
        phone = 0
        try:
            self.cur.execute(query)
            phone = self.cur.fetchone()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return phone

    # Insert admin details
    def insertAdminData(self, data):
        query = 'select count(*) from ' + cfg.TABLE_ADMIN
        cnt = 0
        try:
            self.cur.execute(query)
            cnt = self.cur.fetchone()
        except Exception as e:
            print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))

        if cnt[0] == 0:
            query = 'insert into ' + cfg.TABLE_ADMIN + ' (' + \
                    cfg.KEY_ADMIN_ID + ', ' + cfg.KEY_ADMIN_GYM_NAME + ', ' + cfg.KEY_ADMIN_NAME + ', ' + \
                    cfg.KEY_ADMIN_PHONE + ', ' + cfg.KEY_ADMIN_VALIDITY + ', ' + \
                    cfg.KEY_ADMIN_USERNAME + ' , ' + cfg.KEY_ADMIN_PASSWD + ', ' + \
                    cfg.KEY_ADMIN_STATUS + ') values ("' + data[cfg.FB_KEY_ADMIN_ID] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_GYM_NAME] + '", "' + data[cfg.FB_KEY_ADMIN_NAME] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_PHONE] + '", "' + data[cfg.FB_KEY_ADMIN_VALIDITY] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_USERNAME] + '", sha1("' + data[cfg.FB_KEY_ADMIN_PASSWORD] + '"), "1")'
            try:
                self.cur.execute(query)
                self.db.commit()
            except Exception as e:
                print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))

    # updates login status of admin
    def updateAdminLoginStatus(self, status):
        query = "update " + cfg.TABLE_ADMIN + " set " + cfg.KEY_ADMIN_STATUS + "=" + str(status)

        try:
            self.cur.execute(query)
            self.db.commit()
        except Exception as e:
            print("SQLUserAdminDBOps().updateAdminLoginStatus() :: ERROR :: " + str(e))

    # Get gymId
    def getGymID(self):
        query = 'select ' + cfg.KEY_ADMIN_ID + ' from ' + cfg.TABLE_ADMIN
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

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

    def getStudentData(self, sid):
        query = 'select count(*) from ' + cfg.TABLE_STUDENTS
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res

    # Get first install status
    def getFirstInstallStatus(self):
        query = 'select ' + cfg.KEY_SOFTWARE_FLAG_STATUS + ' from ' + cfg.TABLE_SOFTWARE_FLAG + \
            ' where ' + cfg.KEY_SOFTWARE_FLAG_NAME + '="' + cfg.CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS + '"'
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        if res is None:
            query = 'insert into ' + cfg.TABLE_SOFTWARE_FLAG + ' (' + cfg.KEY_SOFTWARE_FLAG_NAME + ', ' + \
                    cfg.KEY_SOFTWARE_FLAG_STATUS + ') values ("' + cfg.CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS + '", 0) '
            try:
                self.cur.execute(query)
                self.db.commit()
            except Exception as e:
                print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))
        if res is None:
            res = 0
        else:
            res = res[0]
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

    # updates software registry flags
    def updateSoftwareFirstInstallFlag(self, flag, status):
        query = 'update softwareflags set status=' + str(status) + ' where flagname="' + flag + '"'
        try:
            self.cur.execute(query)
        except Exception as e:
            print("SQLAutoSync.updateSoftwareFirstInstallFlag() :: ERROR :: " + str(e))

        self.db.commit()

    def getLocalActionStudentModule(self):
        query = 'select ' + cfg.KEY_ACTION_ACTION + ' from ' + cfg.TABLE_ACTION + ' where module="student" and status=0'
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res