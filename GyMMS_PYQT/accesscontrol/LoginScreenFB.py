import Configuration as cfg
from firebase import firebase


class LoginScreenFB():
    def __init__(self):
        dbUrl = cfg.FB_DB_URL
        self.firebaseDB = firebase.FirebaseApplication(dbUrl, None)

    def checkIfAdminExists(self, phone, passwd):
        pass


