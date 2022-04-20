import pymongo
import os
client = \
    pymongo.MongoClient(
        "mongodb+srv://cebox616:sexologop2p@clustercbx.cdiqu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )

db = client.coppel

new_user = {
    "name": "Marco",
    "age": "27",
    "email": "ma_galeza@hotmail.com",
    "password": "123456",
}

# db.users.insert_one(new_user)
print(os.getenv("MONGO_URL"))
print(os.getenv("API_GET_COMICS"))
print(os.getenv("API_STORE_MY_COMICS"))
print(os.getenv("API_GET_MY_COMICS"))
print(os.getenv("HOME"))
print(db.users.find_one())