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
db_passwd = "s1u5b9_@"
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
KEY_STUDENTS_DUE = 'dueamount'

TABLE_NOTIFICATION = 'Notification'
KEY_NOTIFICATION_NID = 'notifId'
KEY_NOTIFICATION_SID = 'studentId'
KEY_NOTIFICATION_DATETIME = 'dateTime'
KEY_NOTIFICATION_LEVEL = 'level'
KEY_NOTIFICATION_MSG = 'msg'

TABLE_ADMIN = 'GymAdmin'
KEY_ADMIN_ID = 'gymId'
KEY_ADMIN_ROLE = 'memberrole'
KEY_ADMIN_GYM_NAME = 'gymName'
KEY_ADMIN_NAME = 'adminName'
KEY_ADMIN_PHONE = 'phone'
KEY_ADMIN_VALIDITY = 'validity'
KEY_ADMIN_USERNAME = 'username'
KEY_ADMIN_PASSWD = 'passwd'
KEY_ADMIN_STATUS = 'loginstatus'

TABLE_ACTION = 'localaction'
KEY_ACTION_TIME = 'actiontime'
KEY_ACTION_MODULE = 'module'
KEY_ACTION_ACTION = 'action'
KEY_ACTION_STATUS = 'status'

TABLE_SOFTWARE_FLAG = 'softwareflags'
KEY_SOFTWARE_FLAG_NAME = 'flagname'
KEY_SOFTWARE_FLAG_STATUS = 'status'
CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS = 'firstinstallstudent'

TABLE_MSG_NOTIF = 'msgnotif'
KEY_MSG_NOTIF_CNT = 'msgcounter'
KEY_MSG_NOTIF_SID = 'SID'
KEY_MSG_NOTIF_MSG = 'message'

# FIREBASE
# FB_DB_URL = 'https://gymbuddyall.firebaseio.com/'
# FB_GROUP_NAME = 'gymbuddyall/'

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
FB_KEY_STUDENTS_REG_STATUS = 'regstatus'
DB_KEY_STUDENTS_DUE = 'dueamount'

FB_TABLE_NOTIFICATION = 'Notification'
FB_KEY_NOTIFICATION_NID = 'notifId'
FB_KEY_NOTIFICATION_SID = 'studentId'
FB_KEY_NOTIFICATION_DATETIME = 'dateTime'
FB_KEY_NOTIFICATION_LEVEL = 'level'
FB_KEY_NOTIFICATION_MSG = 'msg'

FB_TABLE_ADMIN = 'GymAdmin'
FB_KEY_ADMIN_ID = 'gymId'
FB_KEY_ADMIN_ROLE = 'memberrole'
FB_KEY_ADMIN_GYM_NAME = 'gymName'
FB_KEY_ADMIN_NAME = 'adminName'
FB_KEY_ADMIN_PHONE = 'phone'
FB_KEY_ADMIN_VALIDITY = 'validity'
FB_KEY_ADMIN_USERNAME = 'username'
FB_KEY_ADMIN_PASSWORD = 'passwd'
FB_KEY_ADMIN_STATUS = 'loginstatus'

FB_TABLE_MSG_NOTIF = 'msgnotif'
FB_KEY_MSG_NOTIF_CNT = 'msgcounter'
FB_KEY_MSG_NOTIF_SID = 'SID'
FB_KEY_MSG_NOTIF_MSG = 'message'

# FILE URL
TMP_FILE_URL = "./tmp/tmp.txt"
TMP_FILE_DIR = "./tmp/"
TMP_FILE_PHOTO_DIR = "./tmp/photo/"
SPLASH_SCREEN_URL = './src/splash.jpg'
TITLEBAR_ICON_URL = './src/icons/small_logo.jpg'

# ICONS
IC_SEARCH = './src/icons/ic_search.png'
IC_POWER = './src/icons/ic_power.png'
IC_ADD = './src/icons/ic_add.png'
IC_EDIT = './src/icons/ic_edit.png'
IC_SUBSCRIPTION = './src/icons/ic_subscription.png'
IC_DELETE = './src/icons/ic_clear.png'
IC_TRASH = './src/icons/ic_delete_trash.png'
IC_MESSAGE = './src/icons/ic_message.png'
IC_NOTIFICATION = './src/icons/ic_notification.png'
IC_ADD_NOTIFICATION = './src/icons/ic_add_notification.png'
IC_ADD_PHOTO = './src/icons/ic_add_photo.png'
IC_ADD_COLOR = './src/icons/ic_add_color.png'
IC_SUB_COLOR = './src/icons/ic_sub_color.png'
IC_REFRESH_COLOR = './src/icons/ic_refresh_color.png'
IC_DELETE_COLOR = './src/icons/ic_delete_color.png'
IC_SELECT_ALL = './src/icons/ic_select_all.png'
