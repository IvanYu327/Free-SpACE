from pymongo import MongoClient

from dotenv import load_dotenv
from os import getenv
load_dotenv() 
MONGO_KEY = getenv("MONGO")

#MONGO STUFF --> DO NOT LEAK THIS KEY PLEASE
cluster=MongoClient(MONGO_KEY)
database = cluster["LiquidBingo"]
userCollection = database["Users"]

def loginMethod(username,password):
    
    if (userCollection.count_documents({"_id":username}) == 0):
        print("account dne")
        return
    else:
        userPost = userCollection.find_one({"_id":username})
        if password == userPost["Password"]:
            return True
        else:
            return False

def signUpMethod(username,password):
    if (userCollection.count_documents({"_id":username}) == 0):
        userInitPost = {
            "_id":username,
            "Password":password,
            "Bingos":0
        }
        userCollection.insert_one(userInitPost)
        return True
    else:
        return False




