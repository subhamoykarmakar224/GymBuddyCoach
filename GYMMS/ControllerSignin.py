from SQLUserAdmin import *
import hashlib, os


# Checks if the password entered matches with the user entered password
def checkUserLoginCred(phone, passwd):
    userdb = SQLUserAdmin()
    pwd = userdb.getAdminPasswd(phone)
    pwd = str(pwd[0])
    passwd = str(hashlib.sha1(passwd.encode('utf-8')).hexdigest())
    if passwd.__eq__(pwd):
        updateUserLoginStatus(phone, "1")
        return 1;
    return 0


# Updates the login status of the admin user
def updateUserLoginStatus(phone, status):
    userdb = SQLUserAdmin()
    userdb.updateLoginStatusOfAdmin(phone, status)
    # Delete Current tmp file
    if os._exists(cfg.TMP_FILE_URL):
        os.remove(cfg.TMP_FILE_URL)

    # Save current logged in phone number
    f = open(cfg.TMP_FILE_URL, "w")
    f.write(phone)
    f.close()

    return


# Logout current user
def logoutCurrentUser():
    l = []
    with open(cfg.TMP_FILE_URL) as f:
        l = f.readline()

    phone = l.strip(" ").strip("\n")
    userdb = SQLUserAdmin()
    userdb.updateLoginStatusOfAdmin(phone, "0")
    os.remove(cfg.TMP_FILE_URL)


# if __name__ == '__main__':
#     logoutCurrentUser()
