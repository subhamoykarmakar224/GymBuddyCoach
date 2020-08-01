import eel
import ControllerStudent as students


eel.init("GUI")


@eel.expose
def generate_name_initials(name):
    name = str(name).split(" ")
    initials = ''
    for n in name:
        initials += n[0] + ". "
    return initials


@eel.expose
def getAllStudents():
    return students.getAllStudentsList()


eel.start('index.html', size=(1280, 720))
