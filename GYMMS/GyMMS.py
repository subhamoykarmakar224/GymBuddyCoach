import eel
import ControllerLaunchScreen as launch
import ControllerSignin as signin
import ControllerStudent as students


eel.init("GUI")


# LAUNCH SCREEN
@eel.expose
def getNewUserStatus():
    return launch.getAdminStatus()


# LOGIN TAB
@eel.expose
def checkCredForLogin(phone, passwd):
    return signin.checkUserLoginCred(phone, passwd)


@eel.expose
def checkIsUserLoggedInStatus(phone, passwd):
    return signin.checkUserLoginCred(phone, passwd)

# HOME TAB


# STUDENTS TAB
@eel.expose
def getAllStudents():
    return students.getAllStudentsList()


@eel.expose
def getFilteredStudentResult(queryText):
    return students.getFilteredResult(queryText)


# LOGOUT TAB
@eel.expose
def logoutCurrentUser():
    return signin.logoutCurrentUser()


eel.start('launchscreen.html', size=(1280, 720))
