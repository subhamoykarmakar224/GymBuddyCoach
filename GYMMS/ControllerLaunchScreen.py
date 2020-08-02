from SQLUserAdmin import *


# Checks if the admin user exists
def getAdminStatus():
    userdbop = SQLUserAdmin()
    return userdbop.checkIfUserPresent()


