import eel
import ControllerLaunchScreen as launch
import ControllerSignin as signin
import ControllerStudent as students
import easygui
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkfilebrowser import askopendirname, askopenfilenames, asksaveasfilename


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


@eel.expose
def saveImage(imgSrc, fileName):
    path = easygui.fileopenbox()
    print(path)

    # root = tk.Tk()
    # # style = ttk.Style(root)
    # # style.theme_use("clam")
    # root.minsize()
    # rep = filedialog.askopenfilenames(parent=root, initialdir='/', initialfile='tmp',
    #                                   filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*")])
    # print(rep)
    # root.destroy()
    #

# LOGOUT TAB
@eel.expose
def logoutCurrentUser():
    return signin.logoutCurrentUser()


eel.start('launchscreen.html', size=(1280, 720))
