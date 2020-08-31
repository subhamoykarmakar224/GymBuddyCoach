import students.SQLTabStudents as SQLTabStudents
import Configuration as cfg
import pyrebase


def getFBDB():
    firebase = pyrebase.initialize_app(cfg.FB_CONFIG)
    return firebase.database()


def getSQLDB():
    return SQLTabStudents.SQLTabStudents()


def getOnlineValidity(gymId):
    data = {}
    db = getFBDB()
    res = db.child(cfg.FB_TABLE_ADMIN).child(gymId).get()
    if res.each().__len__() == 0:
        data = {}
    else:
        for r in res.each():
            data[r.key()] = r.val()

    return data


# if __name__ == '__main__':
#     print(getOnlineValidity('BodyShapersGym-2932'))
    # {'adminName': 'Modi', 'gymId': 'BodyShapersGym-2932', 'gymName': 'Body Shapers Gym', 'loginstatus': '0',
    #  'memberrole': 'admin', 'passwd': '1234', 'phone': '+919876543210', 'username': 'mods', 'validity': '31-09-2020'}

# ----TODO :: DELETE ALL BELOW
# Get all students data into Firebase
# def getAllNotification(gymID):
#     data = {}
#     db = getFBDB()
#     res = db.child(cfg.FB_TABLE_NOTIFICATION).child(gymID).get()
#     if res.each().__len__() == 0:
#         data = {}
#     else:
#         for r in res.each():
#             data[r.key()] = r.val()
#
#     return data
#
# def insertAttendence(gymid, sid, d, t):
#     data = {
#         cfg.FB_KEY_ATTENDENCE_DATE: d,
#         cfg.FB_KEY_ATTENDENCE_TIME: t
#     }
#     fbdb = getFBDB()
#     try:
#         fbdb.child(cfg.FB_TABLE_ATTENDENCE).child(gymid).child(sid).child(d).set(data)
#     except Exception as e:
#         return 0
#     try:
#         del fbdb
#     except:
#         print('')
#
#     return 1
#
#
# def deleteNotification(gymid, notifid):
#     fbdb = getFBDB()
#     try:
#         fbdb.child(cfg.FB_TABLE_NOTIFICATION).child(gymid).child(notifid).remove()
#     except Exception as e:
#         return 0
#
#     return 1