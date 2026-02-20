import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("data/spaceinvaders-e0ff8-firebase-adminsdk-fbsvc-af31810396.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spaceinvaders-e0ff8-default-rtdb.europe-west1.firebasedatabase.app/'
})