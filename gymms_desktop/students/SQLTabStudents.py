import mysql.connector as mysql
import Configuration as cfg


class SQLTabStudents():
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

    def deleteStudent(self, id):
        q = 'delete from ' + cfg.TABLE_STUDENTS + ' where ' + cfg.KEY_STUDENTS_SID + '=' + str(id)

    def getLocalActionStudentModule(self):
        query = 'select ' + cfg.KEY_ACTION_ACTION + ' from ' + cfg.TABLE_ACTION + ' where module="student" and status=0'
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchall()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res

    def getGymId(self):
        query = 'select ' + cfg.KEY_ADMIN_ID + ' from ' + cfg.TABLE_ADMIN
        res = ""
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()
        except Exception as e:
            print("SQLAutoSync.getAdminGymId() :: ERROR :: " + str(e))

        return res[0]
