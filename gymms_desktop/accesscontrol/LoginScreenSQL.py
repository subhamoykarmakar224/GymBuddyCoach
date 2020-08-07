import mysql.connector as mysql
import Configuration as cfg


class SQLUserAdmin():
    def __init__(self):
        self.db = mysql.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            passwd=cfg.db_passwd,
            db=cfg.db_gymms
        )
        self.cur = self.db.cursor()

    # Insert admin details
    def insertAdminData(self, data):
        query = 'select count(*) from ' + cfg.TABLE_ADMIN
        cnt = 0
        try:
            self.cur.execute(query)
            cnt = self.cur.fetchone()
        except Exception as e:
            print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))

        if cnt == 0:
            query = 'insert into ' + cfg.TABLE_ADMIN + ' ('+\
                    cfg.KEY_ADMIN_ID+', ' + cfg.KEY_ADMIN_GYM_NAME + ', ' + cfg.KEY_ADMIN_NAME + ', ' + \
                    cfg.KEY_ADMIN_PHONE + ', ' + cfg.KEY_ADMIN_VALIDITY + ', ' + \
                    cfg.KEY_ADMIN_USERNAME + ' , ' + cfg.KEY_ADMIN_PASSWD + ', ' + \
                    cfg.KEY_ADMIN_STATUS + ') values ("' + data[cfg.FB_KEY_ADMIN_ID] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_GYM_NAME] + '", "' + data[cfg.FB_KEY_ADMIN_NAME] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_PHONE] + '", "' + data[cfg.FB_KEY_ADMIN_VALIDITY] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_USERNAME] + '", "' + data[cfg.FB_KEY_ADMIN_PASSWORD] + '", "1")'
            try:
                self.cur.execute(query)
                self.db.commit()
            except Exception as e:
                print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))
            finally:
                self.cur.close()
                self.db.close()

    # returns the user login status
    def checkIfUserPresent(self):
        query = 'select ' + cfg.KEY_ADMIN_STATUS + ' from ' + cfg.TABLE_ADMIN
        res = self.executeQuery(query)
        if len(res) != 0 and res != -404:
            return res[0][-1]
        return -9

    # returns the admin password for checking
    def getAdminPasswd(self, phone):
        query = "select " + cfg.KEY_ADMIN_PASSWD + " from " + cfg.TABLE_ADMIN + " where " + cfg.KEY_ADMIN_PHONE + "='" + phone + "'"
        res = self.executeQuery(query)
        if len(res) == 0:
            return "abc"

        if res != -404:
            return res[0]

    # updates login status of admin
    def updateLoginStatusOfAdmin(self, phone, status):
        query = "update " + cfg.TABLE_ADMIN + " set " + cfg.KEY_ADMIN_STATUS + "='" + status + "' where phone='" + phone + "'"
        try:
            self.cur.execute(query)
            self.db.commit()
        except Exception as e:
            print("SQLUserAdminDBOps().updatesLoginStatusOfAdmin() :: ERROR :: " + str(e))
        finally:
            self.cur.close()
            self.db.close()

    # Executes all query and returns data
    def executeQuery(self, query):
        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            print("SQLUserAdminDBOps() :: ERROR :: " + str(e))
        finally:
            self.cur.close()
            self.db.close()
        return -404
