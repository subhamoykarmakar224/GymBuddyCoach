import students.SQLTabStudents as SQLTabStudents
import Configuration as cfg
import pyrebase, datetime, pytz, time


def getFBDB():
    firebase = pyrebase.initialize_app(cfg.FB_CONFIG)
    return firebase.database()


def getSQLDB():
    return SQLTabStudents.SQLTabStudents()


# Get all students data into Firebase
def getAllStudentsData(gymID):
    data = []
    db = getFBDB()
    res = db.child(cfg.FB_TABLE_STUDENTS).child(gymID).get()
    if res.each() is None:
        return []

    if res.each().__len__() == 0:
        data = []
    else:
        for r in res.each():
            data.append(r.val())
    return data


# Insert students data into Firebase
def insertStudents(student):
    sqldb = getSQLDB()
    gymId = sqldb.getGymId()
    fbdb = getFBDB()
    try:
        fbdb.child(cfg.FB_TABLE_STUDENTS).child(gymId).child(student[cfg.KEY_STUDENTS_SID]).set(student)
    except Exception as e:
        return 0
    try:
        del fbdb
        del sqldb
    except:
        print('')
    return 1


# Update student information
def updateStudents(student):
    sqldb = getSQLDB()
    gymId = sqldb.getGymId()
    fbdb = getFBDB()
    try:
        # update a single value
        # db.child("superuser").child("Kanchan Basu").update({"membershipstart": "01-08-2020"})
        fbdb.child(cfg.FB_TABLE_STUDENTS).child(gymId).child(student[cfg.KEY_STUDENTS_SID]).update(student)
    except Exception as e:
        return 0
    try:
        del fbdb
        del sqldb
    except:
        print('')
    return 1


# Delete student data into Firebase
def deleteStudent(sid):
    sqldb = getSQLDB()
    gymId = sqldb.getGymId()
    fbdb = getFBDB()
    try:
        fbdb.child(cfg.FB_TABLE_STUDENTS).child(gymId).child(sid).remove()
    except Exception as e:
        return 0
    try:
        del fbdb
        del sqldb
    except:
        print('')
    return 1


# Send Notif Message
def sendNotification(indx, sid, msg, gymId):
    data = {
        cfg.FB_KEY_MSG_NOTIF_CNT: indx,
        cfg.FB_KEY_MSG_NOTIF_MSG: msg
    }
    fbdb = getFBDB()
    try:
        fbdb.child(cfg.FB_TABLE_MSG_NOTIF).child(gymId).child(sid[0]).child(indx).set(data)
    except Exception as e:
        return 0
    try:
        del fbdb
    except:
        print('')

    return 1


def uploadAttendenceNotification(gymId, sid, d, starttime):
    # print(gymId, sid, d, starttime) # BodyShapersGym-2932 ID-2932-7e24dabd Attend :: 12-08-2020 :: 1 3:54 PM
    # data = {
    #     'dateTime': "Thu Aug 27 09:30:31 GMT+05:30 2020",
    #     'gymId': "BodyShapersGym-2932",
    #     'level': "GREEN",
    #     'msg': "Student entered the gym.",
    #     'studentId': "ID-2932-7e24dabd"
    # }

    data = {
        'dateTime': getNowDateTimetoCustomFormat(d.split(" :: ")[1], starttime),
        'gymId': gymId,
        'level': "GREEN",
        'msg': "Student entered the gym.",
        'studentId': sid
    }
    fbdb = getFBDB()
    fbdb.child('Notification').child(gymId).push(data)


def getNowDateTimetoCustomFormat(d, t):
    d = d.split("-")
    d = [int(i) for i in d]
    strt = time.strptime(t, '%I:%M %p')
    t = time.strftime('%H:%M', strt)
    t = t.split(':')
    t = [int(j) for j in t]

    now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    gmtdiff = now.strftime('%z')
    gmtdiff = 'GMT' + gmtdiff[0:3] + ':' + gmtdiff[3:]

    regex = '%a %b %d %H:%M:%S %Y'
    res = datetime.datetime(
        d[2], d[1], d[0], t[0], t[1]
    ).strftime(regex)
    res = res.split(' ')
    finalRes = ' '.join(res[:len(res) - 1]) + ' ' + gmtdiff + ' ' +res[-1]
    return finalRes


# if __name__ == '__main__':
#     uploadAttendenceNotification("BodyShapersGym-2932", "ID-2932-7e24dabd", "Attend :: 12-08-2020 :: 1", "3:54 PM")
#     convertDateTimetoCustomFormat()
#     insertStudent({
# 'SID': 'ID-2932-7c2eefa6',
# 'allotedtime': '03:00 PM to 04:30 PM',
# 'membershipvalidity': '2020-09-08',
# 'phone': '+919432743720',
# 'studentage': '1991-10-16',
# 'studentname': 'Subhamoy Karmakar',
# 'regstatus': '1',
# 'dueamount': 0
# })
