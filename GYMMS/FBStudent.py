from firebase import firebase

dbUrl = 'https://gymbuddyall.firebaseio.com/'
groupName = 'gymbuddyall/'
TABLE_STUDENTS = 'Students'
TABLE_MEMBERSHIP = 'MemberShipValidity'
TABLE_ADMIN = 'GymAdmin'
firebaseDB = firebase.FirebaseApplication(dbUrl, None)


def uploadNewStudent():
    data = {
        "SID": "ID-2932-1",
        "studentname": "Subhamoy Karmakar",
        "studentage": "28",
        "allotedtime": "12:15 PM to 1:15 PM",
        "phone": "+919432743720",
        "membershipvalidity": "31-07-2020"
    }

    res = firebaseDB.post(TABLE_STUDENTS, data)
    print(res)


if __name__ == '__main__':
    pass
    # uploadNewStudent()

'''
from firebase import firebase

dbUrl = 'https://homerehabgroup-39322.firebaseio.com/'
groupName = 'homerehabgroup-39322/'
TABLE_ARTISTS = 'artists'
TABLE_STUDENTS = 'students'

firebaseDB = firebase.FirebaseApplication(dbUrl, None)

data = {
    'Name': 'Subhamoy Karmakar',
    'Email': 'abc@gmail.com',
    'Phone': 9432745637
}

# add new data
result = firebaseDB.post(TABLE_STUDENTS, data)
print(result)

# Get data
result = firebaseDB.get(TABLE_ARTISTS, '')
print(result)

# Update data
firebaseDB.put(TABLE_STUDENTS + '/' + '-M4tLLj1P6YpBBqLc4xC', 'Name', 'Sam Furgason')
firebaseDB.put(TABLE_ARTISTS + '/' + '-M4rGLjqQl_gynrukCqI', 'artistName', 'Argha Banerjee')

# Delete Data
firebaseDB.delete(TABLE_STUDENTS, '-M4tLLj1P6YpBBqLc4xC')

'''
