# APP META
APP_NAME = "GYMMS"
APP_DIM_WIDTH = "1280"
APP_DIM_HEIGHT = "720"

# COLORS
bg_dark = "#222831"
bg_light = "#323841"
halo_blue = "#43d9b4"
halo_blue_dark = "#35AD90"
twitter_blue = "#30c8e6"


# MYSQL
db_user = "root"
db_passwd = "cdcju"
db_host = "localhost"
db_gymms = "gymms"

TABLE_STUDENTS = 'Students'
KEY_STUDENTS_SID = 'SID'
KEY_STUDENTS_ALLOTTED_TIME = 'allotedtime'
KEY_STUDENTS_MEMBERSHIP = 'membershipvalidity'
KEY_STUDENTS_PHONE = 'phone'
KEY_STUDENTS_AGE = 'studentage'
KEY_STUDENTS_NAME = 'studentname'
KEY_STUDENTS_REG_STATUS = 'regstatus'

TABLE_NOTIFICATION = 'Notification'
KEY_NOTIFICATION_NID = 'notifId'
KEY_NOTIFICATION_SID = 'studentId'
KEY_NOTIFICATION_DATETIME = 'dateTime'
KEY_NOTIFICATION_LEVEL = 'level'
KEY_NOTIFICATION_MSG = 'msg'

TABLE_ADMIN = 'GymAdmin'
KEY_ADMIN_ID = 'gymId'
KEY_ADMIN_GYM_NAME = 'gymName'
KEY_ADMIN_NAME = 'adminName'
KEY_ADMIN_PHONE = 'phone'
KEY_ADMIN_VALIDITY = 'validity'
KEY_ADMIN_USERNAME = 'username'
KEY_ADMIN_PASSWD = 'passwd'
KEY_ADMIN_STATUS = 'loginstatus'


# FIREBASE
FB_DB_URL = 'https://gymbuddyall.firebaseio.com/'
FB_GROUP_NAME = 'gymbuddyall/'

FB_CONFIG = {
    'apiKey': "AIzaSyAyTO6LAZdEaJh3U2X9WPP_HSAa6sA8dAs",
    'authDomain': "gymbuddyall.firebaseapp.com",
    'databaseURL': "https://gymbuddyall.firebaseio.com",
    'projectId': "gymbuddyall",
    'storageBucket': "gymbuddyall.appspot.com",
    'messagingSenderId': "935818798882",
    'appId': "1:935818798882:web:66a571b3707c2c80db277b",
    'measurementId': "G-4WPH2DVVQ7"
}

FB_TABLE_STUDENTS = 'Students'
FB_KEY_STUDENTS_SID = 'SID'
FB_KEY_STUDENTS_ALLOTTED_TIME = 'allotedtime'
FB_KEY_STUDENTS_MEMBERSHIP = 'membershipvalidity'
FB_KEY_STUDENTS_PHONE = 'phone'
FB_KEY_STUDENTS_AGE = 'studentage'
FB_KEY_STUDENTS_NAME = 'studentname'

FB_TABLE_NOTIFICATION = 'Notification'
FB_KEY_NOTIFICATION_NID = 'notifId'
FB_KEY_NOTIFICATION_SID = 'studentId'
FB_KEY_NOTIFICATION_DATETIME = 'dateTime'
FB_KEY_NOTIFICATION_LEVEL = 'level'
FB_KEY_NOTIFICATION_MSG = 'msg'

FB_TABLE_ADMIN = 'GymAdmin'
FB_KEY_ADMIN_ID = 'gymId'
FB_KEY_ADMIN_GYM_NAME = 'gymName'
FB_KEY_ADMIN_NAME = 'adminName'
FB_KEY_ADMIN_PHONE = 'phone'
FB_KEY_ADMIN_VALIDITY = 'validity'
FB_KEY_ADMIN_USERNAME = 'username'
FB_KEY_ADMIN_PASSWORD = 'passwd'
FB_KEY_ADMIN_STATUS = 'loginstatus'


# FILE URL
TMP_FILE_URL = "./tmp/tmp.txt"
SPLASH_SCREEN_URL = './src/splash.jpg'
TITLEBAR_ICON_URL = './src/icons/small_logo.jpg'
