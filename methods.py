from pymongo import MongoClient
import re
import json
import random


from dotenv import load_dotenv
from os import getenv
load_dotenv() 
MONGO_KEY = getenv("MONGO")

#MONGO STUFF --> DO NOT LEAK THIS KEY PLEASE
cluster=MongoClient(MONGO_KEY)
database = cluster["LiquidBingo"]
userCollection = database["Users"]
masterCollection = database["Admin_Valorant"]

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def loginMethod(email,password):
    
    if (userCollection.count_documents({"_id":email}) == 0):
        return "Account does not exist, consider signing up!"
    else:
        userPost = userCollection.find_one({"_id":email})
        if password == userPost["Password"]:
            return "Success"
        else:
            return "Incorrect username or password!"



def signUpMethod(email,username,password):
    if (userCollection.count_documents({"_id":email}) == 0):
        if checkEmail(email) == False:
            return "Please enter a valid email"
        elif len(username) < 3 or len(username) > 20:
            return "Please enter a username between 3-20 characters."
        elif len(password) < 3 or len(password) > 20:
            return "Please enter a password between 3-20 characters."

        userInitPost = {
            "_id":email,
            "Username":username,
            "Password":password,
            "BingoPts":0,
            "Bingo":{}
        }
        userCollection.insert_one(userInitPost)
        resetBingo(email)
        return "Success"
    else:
        return "Account already exists"

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def resetBingo(email):
    masterPost = masterCollection.find_one({"_id":"Valorant"})
    master = []
    for key in masterPost["items"]:
        master.append(key)
    print(master)

    userCollection.find_one_and_update({"_id":email},{"$set":{"Bingo":random.sample(master,25)}})

def getUsername(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Username"]

def getPassword(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Password"]

def getBingoPts(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["BingoPts"]

def getUserBingo(email):
    userPost = userCollection.find_one({"_id":email})
    return userPost["Bingo"]

def writeMasterJSON():
    masterPost = masterCollection.find_one({"_id":"Valorant"})
    with open ("static/js/master.json", 'w') as f:
        json.dump(masterPost["items"], f, indent=4)

# signUpMethod("ivnyu@gmail.com","weewoo","123")