import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("key/serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL': "https://weapon-recognition-omsk-default-rtdb.firebaseio.com/"
})

ref = db.reference('Users')
data = {
    "1":
        {
            "name": "evenlessio@gmail.com",
            "password": "12345"
        }
}

for key, value in data.items():
    ref.child(key).set(value)