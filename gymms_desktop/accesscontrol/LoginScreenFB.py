import Configuration as cfg
import pyrebase


class LoginScreenFB():
    def __init__(self):
        firebase = pyrebase.initialize_app(cfg.FB_CONFIG)
        self.db = firebase.database()

    def getGymIds(self):
        gymIds = ['']
        res = self.db.child(cfg.FB_TABLE_ADMIN).shallow().get()
        for id in res.val():
            gymIds.append(id)

        return gymIds

    def getGymMetaData(self, phone):
        res = self.db.child(cfg.FB_TABLE_ADMIN)\
            .order_by_child(cfg.FB_KEY_ADMIN_PHONE)\
            .equal_to(phone).get()
        data = {}
        if res.each().__len__() == 0:
            data = {}
        else:
            for r in res.each():
                data = r.val()
        return data

# if __name__ == '__main__':
#     l = LoginScreenFB()
#     l.getGymPassword("+919830616135")

