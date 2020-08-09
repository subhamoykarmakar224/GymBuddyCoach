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

        if cnt[0] == 0:
            query = 'insert into ' + cfg.TABLE_ADMIN + ' (' + cfg.KEY_ADMIN_ID + ', ' + cfg.KEY_ADMIN_ROLE + ', ' + cfg.KEY_ADMIN_GYM_NAME + \
                    ', ' + cfg.KEY_ADMIN_NAME + ', ' + cfg.KEY_ADMIN_PHONE + ', ' + cfg.KEY_ADMIN_VALIDITY +\
                    ', ' + cfg.KEY_ADMIN_USERNAME + ', ' + cfg.KEY_ADMIN_PASSWD + ', ' + cfg.KEY_ADMIN_STATUS + \
                    ') values ( "' + data[cfg.FB_KEY_ADMIN_ID] + '", "' + data[cfg.FB_KEY_ADMIN_ROLE] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_GYM_NAME] + '", "' + data[cfg.FB_KEY_ADMIN_NAME] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_PHONE] + '", "' + data[cfg.FB_KEY_ADMIN_VALIDITY] + '", "' + \
                    data[cfg.FB_KEY_ADMIN_USERNAME] + '", sha1("' + data[cfg.FB_KEY_ADMIN_PASSWORD] + '"), ' + \
                    data[cfg.FB_KEY_ADMIN_STATUS] + ')'
            try:
                self.cur.execute(query)
                self.db.commit()
            except Exception as e:
                print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))
            

    # checks if there is atleast 1 admin user
    def checkIfUserPresent(self):
        query = 'select count(*) from ' + cfg.TABLE_ADMIN
        cnt = 0
        try:
            self.cur.execute(query)
            cnt = self.cur.fetchone()
        except Exception as e:
            print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))
            return False
        

        if cnt[0] > 0:
            return True

        return False

    # returns the admin password for checking
    def getAdminPasswd(self, phone):
        passwd = ''
        query = "select " + cfg.KEY_ADMIN_PASSWD + " from " + cfg.TABLE_ADMIN + " where " + cfg.KEY_ADMIN_PHONE + "='" + phone + "'"
        try:
            self.cur.execute(query)
            passwd = self.cur.fetchone()
        except Exception as e:
            print("LoginScreenSQL.insertAdminData() :: ERROR :: " + str(e))
            return ('abc',)
        

        return passwd

    # Get Gym Id of admin
    def getGymID(self):
        query = "select " + cfg.KEY_ADMIN_ID + " from " + cfg.TABLE_ADMIN
        res = ""
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLUserAdminDBOps().updatesLoginStatusOfAdmin() :: ERROR :: " + str(e))
        
            return res

        return res

    # updates login status of admin
    def updateAdminLoginStatus(self, status):
        query = "update " + cfg.TABLE_ADMIN + " set " + cfg.KEY_ADMIN_STATUS + "=" + str(status)
        cur = self.db.cursor()
        try:
            cur.execute(query)
            self.db.commit()
        except Exception as e:
            print("SQLUserAdminDBOps().updateAdminLoginStatus() :: ERROR :: " + str(e))
        finally:
            cur.close()
            self.db.close()

    # Get the logged in status of the last user
    def getLoginStatus(self, phone):
        query = "select " + cfg.KEY_ADMIN_STATUS + " from " + cfg.TABLE_ADMIN + " where phone='" + phone + "'"
        res = 0
        try:
            self.cur.execute(query)
            res = self.cur.fetchone()[0]
        except Exception as e:
            print("SQLUserAdminDBOps().updatesLoginStatusOfAdmin() :: ERROR :: " + str(e))
        
            return res

        return res

    # Get information on the logged in User
    def getLoggedInData(self, phone):
        query = "select " + cfg.KEY_ADMIN_ID + ", " + cfg.KEY_ADMIN_GYM_NAME + ", " + cfg.KEY_ADMIN_NAME + ", " \
                + cfg.KEY_ADMIN_USERNAME + " from " + cfg.TABLE_ADMIN + " where phone='" + phone + "'"
        res = {}
        data = ()
        try:
            self.cur.execute(query)
            data = self.cur.fetchone()
        except Exception as e:
            print("SQLUserAdminDBOps().updatesLoginStatusOfAdmin() :: ERROR :: " + str(e))
        
        if data == ():
            res = {
                cfg.KEY_ADMIN_ID: "",
                cfg.KEY_ADMIN_GYM_NAME: "",
                cfg.KEY_ADMIN_NAME: "",
                cfg.KEY_ADMIN_USERNAME: "",
            }
        else:
            res = {
                cfg.KEY_ADMIN_ID: data[0],
                cfg.KEY_ADMIN_GYM_NAME: data[1],
                cfg.KEY_ADMIN_NAME: data[2],
                cfg.KEY_ADMIN_USERNAME: data[3],
            }

        return res

# if __name__ == '__main__':
#     sq = SQLUserAdmin()
    # data = {'adminName': 'Kanchan Basu', 'gymId': 'BodyShapersGym-2932', 'gymName': 'Body Shapers Gymnasium',
    #         'loginstatus': '0', 'passwd': '1234', 'phone': '+919432743720', 'username': 'kd', 'validity': '31-08-2020'}
    # sq.insertAdminData(data)
    # print("S : ", sq.getLoginStatus("+919876543210"))
