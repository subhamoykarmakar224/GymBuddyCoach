# https://github.com/thisbejim/Pyrebase

import pyrebase
import Configuration as cfg

firebaseConfig = {
    'apiKey': "AIzaSyAyTO6LAZdEaJh3U2X9WPP_HSAa6sA8dAs",
    'authDomain': "gymbuddyall.firebaseapp.com",
    'databaseURL': "https://gymbuddyall.firebaseio.com",
    'projectId': "gymbuddyall",
    'storageBucket': "gymbuddyall.appspot.com",
    'messagingSenderId': "935818798882",
    'appId': "1:935818798882:web:6e4bfeaf0ee239b7db277b",
    'measurementId': "G-FQ8JB6MY9F"
}

firebase = pyrebase.initialize_app(cfg.FB_CONFIG)

# Used to access the authentication modules of firebase
# auth = firebase.auth()

# For DB
db = firebase.database()


def signUp():
    print("Sign Up...")
    email = input("Enter Phone :: ")
    passwd = input("Enter Password :: ")
    try:
        user = auth.create_user_with_email_and_password(email, passwd)
        print("New User created!")
    except:
        print("Email already exists!")


def login():
    print("Log in...")
    email = input("Enter Phone :: ")
    passwd = input("Enter Password :: ")
    try:
        login = auth.sign_in_with_email_and_password(email, passwd)
        print(auth.get_account_info(login['idToken']))
        '''
        {
        'kind': 'identitytoolkit#GetAccountInfoResponse', 
        'users': [{
            'localId': '57xISQ1zcyZZKGw9CUX5f4XXRjo2', 
            'email': 'subhamoykarmakar224@gmail.com', 
            'passwordHash': 'UkVEQUNURUQ=', 
            'emailVerified': False, 
            'passwordUpdatedAt': 1596520581441, 
            'providerUserInfo': [{
                'providerId': 'password', 
                'federatedId': 'subhamoykarmakar224@gmail.com', 
                'email': 'subhamoykarmakar224@gmail.com', 
                'rawId': 'subhamoykarmakar224@gmail.com'
            }], 
            'validSince': '1596520581', 
            'lastLoginAt': '1596520581441', 
            'createdAt': '1596520581441', 
            'lastRefreshAt': '2020-08-04T05:56:21.441Z'
        }]
        }

        '''
        print("Logged in!")
    except:
        print("Wrong email/password!")


def insertData():
    # Insert Data
    # data = {"name": "Subhamoy Karmakar", "age": "28", "address": "Behala, Kolkata"}
    data = {"name": "Sheenjini Ghosh", "age": "27", "address": "Baguihati, Kolkata"}
    # data = {"name": "Kanchan Basu", "age": "41", "address": "Bacharam Chatterjee Road, Kolkata"}
    # db.push(data)

    # Insert Data with own key
    # db.child("superuser").push(data)
    db.child("superuser").child(data["name"]).set(data)


def updateDate():
    # update a single value
    # db.child("superuser").child("Kanchan Basu").update({"membershipstart": "01-08-2020"})

    # update multiple values
    # data = {
    #     "superuser/Kanchan Basu/": {"membershipstart": "10-08-2020"},
    #     "superuser/Kanchan Basu/": {"age": 40}
    # }
    # db.update(data)
    students_list = db.child("Students").get()
    for student in students_list.each():
        # print(student.key())
        # print(student.val())
        if student.val()['studentname'] == 'Sheenjini Ghosh':
            print(student.val())


def deleteData():
    db.child("superuser").child("Sheenjini Ghosh").remove()


def selectData():
    # students = db.child("superuser").shallow().get()
    # print(students.val())

    students = db.child("superuser").get()
    print(students.val())


def advancedSelectData():
    # students = db.child("superuser").order_by_child("name").equal_to("Subhamoy Karmakar").get()
    # students = db.child("superuser").order_by_child("age").equal_to("41").get()
    # students = db.child("superuser").order_by_child("age").equal_to("41").limit_to_first(1).get()
    # students = db.child("superuser").order_by_child("age").equal_to("41").limit_to_last(1).get()
    # students = db.child("superuser").order_by_child("age").end_at("30").get() # <= operation
    # students = db.child("superuser").order_by_child("age").start_at("30").get() # >= operation
    # students = db.child("superuser").order_by_child("age").start_at("28").end_at("45").get() # between inclusive operation

    students = db.child("superuser").order_by_key().get() # select all from key

    print(students.each().__len__())
    for s in students.each():
        print(s.key())
        print(s.val())


def demoInsertGymAdmin():
    data = {
        'adminName': "Modi",
        'gymId': "BodyShapersGym-2932",
        'memberrole': 'admin',
        'gymName': "Body Shapers Gym",
        'loginstatus': "0",
        'passwd': "1234",
        'phone': "+919876543210",
        'username': "mods",
        'validity': "31-09-2020"
    }

    # Insert Data with own key
    # db.child("superuser").push(data)
    db.child("GymAdmin").child(data["gymId"]).set(data)


def updateGymAdmin():
    db.child("GymAdmin") \
        .child("BodyShapersGym-2932")\
        .update({"phone": "+919432743720"})


def demoInsertStudents():
    data = {
        "SID": "ID-2932-1",
        "studentname": "Subhamoy Karmakar",
        "studentage": "28",
        "allotedtime": "4:15 PM to 6:15 PM",
        "phone": "+919432743720",
        "membershipvalidity": "31-10-2020",
        "regstatus": "1",
        "dueamount": "0"
    }

    # Insert Data with own key
    # db.child("superuser").push(data)
    db.child("Students").child("BodyShapersGym-2932").child(data['SID']).set(data)


if __name__ == '__main__':
    pass
    # demoInsertStudents()
