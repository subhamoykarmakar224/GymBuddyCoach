import sync.SQLAutoSync as SQLAutoSync
import Configuration as cfg
import pyrebase


class FBAutoSync():
    def __init__(self):
        firebase = pyrebase.initialize_app(cfg.FB_CONFIG)
        self.db = firebase.database()

        self.sql = SQLAutoSync.SQLAutoSync()

    def getGymMetaData(self):
        phone = self.sql.getAdminPhone()
        data = {}
        if phone == 0:
            return data

        phone = phone[0]

        res = self.db.child(cfg.FB_TABLE_ADMIN) \
            .order_by_child(cfg.FB_KEY_ADMIN_PHONE) \
            .equal_to(phone).get()
        if res.each().__len__() == 0:
            data = {}
        else:
            for r in res.each():
                data = r.val()
        return data

    def getAllStudentsData(self, gymID):
        data = []
        res = self.db.child(cfg.FB_TABLE_STUDENTS).child(gymID).get()
        if res.each().__len__() == 0:
            data = []
        else:
            for r in res.each():
                data.append(r.val())
        return data

    def getAllNotificationData(self, gymID):
        data = []
        res = self.db.child(cfg.FB_TABLE_NOTIFICATION).child(gymID).get()
        if res.each().__len__() == 0:
            data = []
        else:
            for r in res.each():
                data.append(r.val())
        return data

    def getAllAttendenceData(self, gymID):
        data = {}
        res = self.db.child(cfg.FB_TABLE_ATTENDENCE).child(gymID).get()
        if res.each().__len__() == 0:
            data = {}
        else:
            for r in res.each():
                data[r.key()]= r.val()
        return data



# if __name__ == '__main__':
#     l = FBAutoSync()
    # print(l.getAllStudentsData("BodyShapersGym-2932"))
    # print(l.getAllNotificationData("BodyShapersGym-2932"))
    # print(l.getAllAttendenceData("BodyShapersGym-2932"))
