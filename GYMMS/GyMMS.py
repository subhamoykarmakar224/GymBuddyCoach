import eel
import ControllerLaunchScreen as launch
import ControllerStudent as students


eel.init("GUI")


@eel.expose
def getLoginStatus():
    return


@eel.expose
def getAllStudents():
    return students.getAllStudentsList()


@eel.expose
def getFilteredStudentResult(queryText):
    return students.getFilteredResult(queryText)


eel.start('launchscreen.html', size=(1280, 720))
